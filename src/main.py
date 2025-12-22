import cv2
import numpy as np
from blocks import split_into_blocks, merge_blocks
from transform import compress_block

q = 20

#read convert grayscale, write new mp4
def main():
    #set these to input paths later
    inputFile = "./rock.mp4"
    outputFile = "./output.mp4"

    cap = cv2.VideoCapture(inputFile)
    if not cap.isOpened():
        raise RuntimeError("Failed to open input video")

    #get metadata with cv2
    fps = cap.get(cv2.CAP_PROP_FPS)
    width, height = 320, 240

    #set up writer(bgr for discord compatability)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(
        outputFile,
        fourcc,
        fps,
        (width, height),
        isColor=True
    )

    frameCount = 0
    writtenFrames = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        #skip every other frame for performance
        if frameCount % 2 != 0:
            frameCount += 1
            continue

        #downscale frame for performance
        frame = cv2.resize(frame, (320, 240))

        #get gray intensity
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #split into 8x8 numpy blocks and grayscale them
        blocks, shape = split_into_blocks(gray)

        #apply DCT + quantization compression to each block
        compressedBlocks = []
        for block in blocks:
            compressed = compress_block(block, q)
            compressedBlocks.append(compressed)

        #put them back together
        reconstructed = merge_blocks(compressedBlocks, shape)

        #put into BGR
        bgr = cv2.cvtColor(reconstructed, cv2.COLOR_GRAY2BGR)

        writer.write(bgr)
        writtenFrames += 1

        frameCount += 1

    #note we must re-encode with ffmpeg for discord compatability
    print(f"Wrote {frameCount} frame to {outputFile}")

if __name__ == "__main__":
    main()
