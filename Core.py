import math

import numpy as np
import cv2 as cv
import ctypes as ct
from pathlib import Path

import time
import asyncio


class Core:
    elapsedTime = 0
    left = []
    right = []
    returnedImage = []
    chosenASM = False
    asmDll= ct.cdll.LoadLibrary('{}\DllCPP.dll'.format(Path().absolute()))
    async def calculatePieceOfImage(self, i):

        # Get 4 pixels from left image
        pixL = self.getPixelOfFlattenedArray(self.left, i)
        pixL2 = self.getPixelOfFlattenedArray(self.left, i + 1)
        pixL3 = self.getPixelOfFlattenedArray(self.left, i + 2)
        pixL4 = self.getPixelOfFlattenedArray(self.left, i + 3)
        pixL = (ct.c_int * len(pixL))(*pixL)
        pixL2 = (ct.c_int * len(pixL2))(*pixL2)
        pixL3 = (ct.c_int * len(pixL3))(*pixL3)
        pixL4 = (ct.c_int * len(pixL4))(*pixL4)
        # Get 4 pixels from right image
        pixR = self.getPixelOfFlattenedArray(self.right, i)
        pixR2 = self.getPixelOfFlattenedArray(self.right, i + 1)
        pixR3 = self.getPixelOfFlattenedArray(self.right, i + 2)
        pixR4 = self.getPixelOfFlattenedArray(self.right, i + 3)
        pixR = (ct.c_int * len(pixL))(*pixR)
        pixR2 = (ct.c_int * len(pixL2))(*pixR2)
        pixR3 = (ct.c_int * len(pixL3))(*pixR3)
        pixR4 = (ct.c_int * len(pixL4))(*pixR4)
        passedList = [pixL, pixL2, pixL3, pixL4, pixR, pixR2, pixR3, pixR4]

        passedCArray = (ct.c_uint * 3 * 8)(*(tuple(i) for i in passedList))
        self.asmDll.Calculate(passedCArray)

        rpix = self.getPixelOfFlattenedArray(self.returnedImage, i)
        rpix2 = self.getPixelOfFlattenedArray(self.returnedImage, i + 1)
        rpix3 = self.getPixelOfFlattenedArray(self.returnedImage, i + 2)
        rpix4 = self.getPixelOfFlattenedArray(self.returnedImage, i + 3)

        rpix[0] = int(passedCArray[0][0])
        rpix[1] = int(passedCArray[0][1])
        rpix[2] = int(passedCArray[0][2])

        rpix2[0] = int(passedCArray[1][0])
        rpix2[1] = int(passedCArray[1][1])
        rpix2[2] = int(passedCArray[1][2])

        rpix3[0] = int(passedCArray[2][0])
        rpix3[1] = int(passedCArray[2][1])
        rpix3[2] = int(passedCArray[2][2])

        rpix4[0] = int(passedCArray[3][0])
        rpix4[1] = int(passedCArray[3][1])
        rpix4[2] = int(passedCArray[3][2])

    async def anglifyASM(self):
        semaphore = asyncio.Semaphore(self.systemThreads)

        height = self.left.shape[0]
        width = self.left.shape[1]
        self.returnedImage = np.zeros([height, width, 3], dtype='uint8')

        time_start = time.time()
        tasks = [self.calculatePieceOfImage(i)for i in range(0, width * height, 4)]

        async with semaphore:
            await asyncio.gather(*tasks, return_exceptions=True)

        self.elapsedTime = time.time() - time_start
        return self.returnedImage


    def moveTenToRight(self, img):
        height = img.shape[0]
        width = img.shape[1]
        returnedImage = np.zeros([height, width, 3], dtype=ct.c_int)
        for i in range(0, height):
            for j in range(0, width - 5):
                returnedImage[i][j][2] = img[i][j + 5][2]
                returnedImage[i][j][1] = img[i][j + 5][1]
                returnedImage[i][j][0] = img[i][j + 5][0]
        return returnedImage


    def moveTenToLeft(self, img):
        height = img.shape[0]
        width = img.shape[1]
        returnedImage = np.zeros([height, width, 3], dtype=ct.c_int)
        for i in range(0, height):
            for j in range(0, width - 5):
                returnedImage[i][j + 5][2] = img[i][j][2]
                returnedImage[i][j + 5][1] = img[i][j][1]
                returnedImage[i][j + 5][0] = img[i][j][0]
        return returnedImage


    def cutImage(self, img):
        height = img.shape[0]
        width = img.shape[1] - 10
        returnedImage = np.zeros([height, width, 3],dtype=np.uint8)
        for i in range(0, height):
            for j in range(0, width):
                returnedImage[i][j][2] = img[i][j + 5][2]
                returnedImage[i][j][1] = img[i][j + 5][1]
                returnedImage[i][j][0] = img[i][j + 5][0]
        return returnedImage


    def getPixelOfFlattenedArray(self, img, idx):
        height = img.shape[0]
        width = img.shape[1]
        if idx >= height*width:
            return [0, 0, 0]
        row = int(idx / width)
        col = idx % width
        return img[row][col]

    def anaglify(self, image):
        if self.chosenASM == True:
            self.asmDll = ct.WinDLL('{}\DllASM.dll'.format(Path().absolute()))
        self.left = self.moveTenToLeft(image)
        self.right = self.moveTenToRight(image)
        anaglified = asyncio.run(self.anglifyASM())
        anaglified = self.cutImage(anaglified)
        return anaglified


# img = cv.imread('sample.jpg')
# left = moveTenToLeft(img)
# right = moveTenToRight(img)
# anaglified = anglifyASM(left, right)
# anaglified = cutImage(anaglified)
# cv.imshow('anaglif', anaglified)
# cv.imwrite('result.jpg', anaglified)
# cv.waitKey(0)