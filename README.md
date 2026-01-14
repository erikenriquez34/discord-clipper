# Discord Clipper

Performs a lossy video compression algorithm to reduce the video size to 8MB, which is Discord's upload limit for users without Nitro. The program takes an input video file, compresses each frame using an 8×8 block-based transform, and outputs a compressed MP4 video that is still compatible with Discord playback.

# Current State:

First, the frames are read using OpenCV. They are then resized to a lower resolution (640x360) to reduce the number of blocks processed. This was done to help improve performance and speed, but it will be changed to the original resolution when I can make this faster (probably through multithreading). We split each frame into 8x8 blocks and apply a Discrete Cosine Transform (DCT), which is used to discard the high-frequency information. We then merge the blocks back together. The compression does not yet adapt to 8MB; the compression right now is a 'good enough' value that will make the video size very small (maybe through estimation methods or multiple compressions, we can approach the 8mb target).

The product is a compressed video encoding, but it has no sound because OpenCV writes video only. So, we use a Linux tool, FFmpeg, to add the original audio to the compressed file. The output is a compressed video with the original sound. If FFmpeg is not available, the program falls back to outputting a video-only output, which will have no sound.

# Dependencies:
* Python
* NumPy
* OpenCV
* FFmpeg (recommended, for audio)

# Installation and Setup:
Clone the repository

    git clone https://github.com/erikenriquez34/discord-clipper
Navigate to the project and install the project dependencies

    cd ./discord-clipper
Create a virtual environment

    python3 -m venv venv
    source venv/bin/activate
Install Python dependencies

    pip install -r requirements.txt
Install FFmpeg (recommended)

    sudo apt install ffmpeg
# Usage
Remember to be in the virtual environment

    source venv/bin/activate
Run the program by passing the input video file as an argument:

    python3 src/main.py input.mp4
Output will be stored in a file with the same name, and _compressed added. So in the previous example, the output is `input_compressed.mp4`.
