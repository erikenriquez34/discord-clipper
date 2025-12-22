import numpy as np
import cv2

BLOCK_SIZE = 8

def dct_2d(block):
    #apply discrete cosine transform to a block
    block = block.astype(np.float32)
    return cv2.dct(block)


def idct_2d(block):
    #inverse 2D dct
    return cv2.idct(block)


def quantize(block, q):
    #quantize dct coefficient
    return np.round(block / q)


def dequantize(block, q):
    #reverse quantization.
    return block * q


def compress_block(block, q):
    #combine function to get compression-decompression pipeline for a single block
    dct = dct_2d(block)
    q_block = quantize(dct, q)
    deq = dequantize(q_block, q)
    recon = idct_2d(deq)

    #set values back to valid pixel range
    recon = np.clip(recon, 0, 255)
    return recon.astype(np.uint8)
