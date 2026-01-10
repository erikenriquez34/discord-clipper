import cv2
import os
import subprocess
import shutil
import argparse
from pathlib import Path
from blocks import split_into_blocks, merge_blocks
from transform import compress_block_parallel
from multiprocessing import Pool, cpu_count

#low value is more compression, high value is more quality
compressionFactor = 5

#multiprocess workers
pool = Pool(processes=cpu_count())

def parse_args():
    parser = argparse.ArgumentParser(
        description="Video compression project"
    )
    parser.add_argument(
        "input",
        type=str,
        help="Path to input video file"
    )
    return parser.parse_args()

def main():
    #set temp path if not yet made
    os.makedirs("temp", exist_ok=True)
    args = parse_args()

    #read input from args
    inputFile = args.input
    outputFile = "./temp/compressed.mp4"

    cap = cv2.VideoCapture(inputFile)
    if not cap.isOpened():
        raise RuntimeError("Failed to open input video:", inputFile)

    #get metadata with cv2
    fps = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    #for progress print statement
    totalFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    #set up writer
    writer = cv2.VideoWriter(
        outputFile,
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        (width, height),
        isColor=True
    )

    frameCount = 0
    print("Compressing...")

    #main compression loop
    with Pool(processes=cpu_count()) as pool:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frameCount % 60 == 0:
                percent = (frameCount / totalFrames) * 100
                print(f"Progress: {percent:.1f}%")

            #split each channel into 8x8 blocks, compress, and merge back
            compressedChannels = []

            for ch in range(3): #for each channel BGR
                channel = frame[:, :, ch]
                blocks, shape = split_into_blocks(channel)

                compressedBlocks = pool.map(
                    compress_block_parallel, 
                    [(block, compressionFactor) for block in blocks])
                
                reconstructed = merge_blocks(compressedBlocks, shape)
                compressedChannels.append(reconstructed)

            #stack channels back into BGR frame
            bgr = cv2.merge(compressedChannels)
            writer.write(bgr)
            frameCount += 1

    cap.release()
    writer.release()
    
    result = mergeAudio(outputFile, inputFile)
    print("\nCompressed", result, "down to", os.path.getsize(result), "bytes")

#use ffmpeg to add audio to video
def mergeAudio(outputFile, inputFile):
    inputPath = Path(inputFile)
    result = (inputPath.stem + "_compressed" + inputPath.suffix)

    if shutil.which("ffmpeg") is None:
        print("FFmpeg not found! Output will have no audio.")
        shutil.copy(outputFile, result)
        return result
    
    #tuned for discord uploads
    subprocess.run([
        "ffmpeg", "-y",
        "-i", outputFile,
        "-i", inputFile,
        "-c:v", "libx264",
        "-preset", "fast",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-c:a", "aac",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        result
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return result

if __name__ == "__main__":
    main()
