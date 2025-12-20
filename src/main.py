import cv2
import os

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
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

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
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        #get gray intensity
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #convert bgr
        bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        #write to output
        writer.write(bgr)
        frameCount += 1

    cap.release()
    writer.release()

    print(f"Wrote {frameCount} to {outputFile}")

if __name__ == "__main__":
    main()
