import sys
import numpy as np
import cv2

def main():
  if len(sys.argv) != 4:
    print("Usage: python3 grid2png.py <lookup table> <input> <output>")
    exit(1)
  mat = readGrid(sys.argv[2],12000,12000)
  writeImg(sys.argv[3],mat)


def readGrid(grid,NX,NY):
  fp = open(grid,"rb")
  mat = np.zeros((NX,NY),dtype=np.uint16)
  print("Loading image...")
  for i in range(NX):
    for j in range(NY):
      mat[i,j] = (int.from_bytes(fp.read(2),byteorder='big',signed=False))*32
  return mat

def writeImg(filename,img):
  print("Writing image...")
  cv2.imwrite(filename,img)

if __name__ == '__main__':
    main()
