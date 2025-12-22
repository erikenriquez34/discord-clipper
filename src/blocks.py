import numpy as np

BLOCK_SIZE = 8

def split_into_blocks(frame):
    #split into 8x8 blocks and return a list of them
    h, w = frame.shape
    h_crop = h - (h % BLOCK_SIZE)
    w_crop = w - (w % BLOCK_SIZE)

    blocks = []
    for y in range(0, h_crop, BLOCK_SIZE):
        for x in range(0, w_crop, BLOCK_SIZE):
            block = frame[y:y+BLOCK_SIZE, x:x+BLOCK_SIZE]
            blocks.append(block.copy())

    return blocks, (h_crop, w_crop)


def merge_blocks(blocks, shape):
    #rebuild the frame from the blocks
    h, w = shape
    frame = np.zeros((h, w), dtype=np.uint8)

    idx = 0
    for y in range(0, h, BLOCK_SIZE):
        for x in range(0, w, BLOCK_SIZE):
            frame[y:y+BLOCK_SIZE, x:x+BLOCK_SIZE] = blocks[idx]
            idx += 1

    return frame
