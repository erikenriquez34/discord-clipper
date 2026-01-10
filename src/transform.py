import numpy as np
import cv2

#8x8 blocks
BLOCK_SIZE = 8

#apply discrete cosine transform to a block
def dct_2d(block):
    block = block.astype(np.float32)
    return cv2.dct(block)

#inverse 2D dct
def idct_2d(block):
    return cv2.idct(block)

#quantize dct coefficient
def quantize(block, q):
    return np.round(block / q)

#reverse quantization.
def dequantize(block, q):
    return block * q

#combine function to get compression-decompression pipeline for a single block
def compress_block(block, q):
    dct = dct_2d(block)
    q_block = quantize(dct, q)
    deq = dequantize(q_block, q)
    recon = idct_2d(deq)

    #set values back to valid pixel range
    recon = np.clip(recon, 0, 255)
    return recon.astype(np.uint8)

#multitprocess compression call
def compress_block_parallel(args):
    block, q = args
    return compress_block(block, q)