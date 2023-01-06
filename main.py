import math

import numpy as np
import cv2 as cv
import ctypes as ct


class tabASM(ct.Structure):
    fields = [("B", ct.POINTER(ct.c_int)), ("G", ct.POINTER(ct.c_int)), ("R", ct.POINTER(ct.c_int))]


def anglifyASM(left, right):
    height = left.shape[0]
    width = left.shape[1]
    returnedImage = np.zeros([height, width, 3], dtype='uint8')
    asmDll = ct.WinDLL("C:\\Users\\jakub\\OneDrive\\Pulpit\\ASM PROJEKT\\JA-Anglyph-AsmPython\\DllAsm.dll")

    for i in range(0, width * height, 4):
        # Get 4 pixels from left image
        pixL = getPixelOfFlattenedArray(left, i)
        pixL2 = getPixelOfFlattenedArray(left, i + 1)
        pixL3 = getPixelOfFlattenedArray(left, i + 2)
        pixL4 = getPixelOfFlattenedArray(left, i + 3)
        pixL = (ct.c_int * len(pixL))(*pixL)
        pixL2 = (ct.c_int * len(pixL2))(*pixL2)
        pixL3 = (ct.c_int * len(pixL3))(*pixL3)
        pixL4 = (ct.c_int * len(pixL4))(*pixL4)
        # Get 4 pixels from right image
        pixR = getPixelOfFlattenedArray(right, i)
        pixR2 = getPixelOfFlattenedArray(right, i + 1)
        pixR3 = getPixelOfFlattenedArray(right, i + 2)
        pixR4 = getPixelOfFlattenedArray(right, i + 3)
        pixR = (ct.c_int * len(pixL))(*pixR)
        pixR2 = (ct.c_int * len(pixL2))(*pixR2)
        pixR3 = (ct.c_int * len(pixL3))(*pixR3)
        pixR4 = (ct.c_int * len(pixL4))(*pixR4)
        passedList = [pixL, pixL2, pixL3, pixL4, pixR, pixR2, pixR3, pixR4]
        # # Create 3 arrays off left BGR values
        # pyLarrB = [pixL[0], pixL2[0], pixL3[0], pixL4[0]]
        # pyLarrG = [pixL[1], pixL2[1], pixL3[1], pixL4[1]]
        # pyLarrR = [pixL[2], pixL2[2], pixL3[2], pixL4[2]]
        #
        # # Create 3 arrays off right BGR values
        # pyRarrB = [pixR[0], pixR2[0], pixR3[0], pixR4[0]]
        # pyRarrG = [pixR[1], pixR2[1], pixR3[1], pixR4[1]]
        # pyRarrR = [pixR[2], pixR2[2], pixR3[2], pixR4[2]]
        #
        # #?
        # arrLB = (ct.c_int * len(pyLarrB))(*pyLarrB)
        # arrLG = (ct.c_int * len(pyLarrG))(*pyLarrG)
        # arrLR = (ct.c_int * len(pyLarrR))(*pyLarrR)
        #
        # arrRB = (ct.c_int * len(pyRarrB))(*pyRarrB)
        # arrRG = (ct.c_int * len(pyRarrG))(*pyRarrG)
        # arrRR = (ct.c_int * len(pyRarrR))(*pyRarrR)

        # #Creating struct of arrays
        # arrLeftStruct = tabASM(arrLB, arrLG, arrLR)
        # arrRightStruct = tabASM(arrRB, arrRG, arrRR)
        #
        # #Passing struct to arrays
        # asmDll.Calculate(arrLeftStruct)
        # asmDll.Calculate(arrRightStruct)
        #passedCArray = (ct.POINTER(ct.c_int) * len(passedList))(*passedList)
        passedCArray = (ct.c_uint * 3 * 8)(*(tuple(i) for i in passedList))
        #print(passedCArray)
        #print(passedCArray[2][:])

        asmDll.Calculate(passedCArray)
        #print(passedCArray[2][:])

        #print([passedCArray[0][0], passedCArray[0][1], passedCArray[0][2]])
        # #TODO: fix the bug with conversion and fix the every 4-th pixel wrong value (?)
        # parsedRArray = ct.cast(arrLB, ct.POINTER(ct.c_int * 4))
        # parsedGBArray = ct.cast(arrRB, ct.POINTER(ct.c_int * 4))
        # pythonBGList = parsedGBArray.contents[:]
        # pythonRList = parsedRArray.contents[:]
        #
        rpix = getPixelOfFlattenedArray(returnedImage, i)
        rpix2 = getPixelOfFlattenedArray(returnedImage, i + 1)
        rpix3 = getPixelOfFlattenedArray(returnedImage, i + 2)
        rpix4 = getPixelOfFlattenedArray(returnedImage, i + 3)

        rpix[0] = int(passedCArray[0][0])
        rpix[1] = int(passedCArray[0][1])
        rpix[2] = int(passedCArray[0][2])
        #print (rpix[2])
        #
        rpix2[0] = int(passedCArray[1][0])
        rpix2[1] = int(passedCArray[1][1])
        rpix2[2] = int(passedCArray[1][2])

        rpix3[0] = int(passedCArray[2][0])
        rpix3[1] = int(passedCArray[2][1])
        rpix3[2] = int(passedCArray[2][2])
        #
        rpix4[0] = int(passedCArray[3][0])
        rpix4[1] = int(passedCArray[3][1])
        rpix4[2] = int(passedCArray[3][2])
    return returnedImage


def moveTenToRight(img):
    height = img.shape[0]
    width = img.shape[1]
    returnedImage = np.zeros([height, width, 3], dtype=ct.c_int)
    for i in range(0, height):
        for j in range(0, width - 5):
            returnedImage[i][j][2] = img[i][j + 5][2]
            returnedImage[i][j][1] = img[i][j + 5][1]
            returnedImage[i][j][0] = img[i][j + 5][0]
    return returnedImage


def moveTenToLeft(img):
    height = img.shape[0]
    width = img.shape[1]
    returnedImage = np.zeros([height, width, 3], dtype=ct.c_int)
    for i in range(0, height):
        for j in range(0, width - 5):
            returnedImage[i][j + 5][2] = img[i][j][2]
            returnedImage[i][j + 5][1] = img[i][j][1]
            returnedImage[i][j + 5][0] = img[i][j][0]
    return returnedImage


def cutImage(img):
    height = img.shape[0]
    width = img.shape[1] - 10
    returnedImage = np.zeros([height, width, 3],dtype=np.uint8)
    for i in range(0, height):
        for j in range(0, width):
            returnedImage[i][j][2] = img[i][j + 5][2]
            returnedImage[i][j][1] = img[i][j + 5][1]
            returnedImage[i][j][0] = img[i][j + 5][0]
    return returnedImage


def getPixelOfFlattenedArray(img, idx):
    height = img.shape[0]
    width = img.shape[1]
    if idx >= height*width:
        return [0, 0, 0]
    row = int(idx / width)
    col = idx % width
    return img[row][col]


img = cv.imread('sample2.jpg')
left = moveTenToLeft(img)
right = moveTenToRight(img)
anaglified = anglifyASM(left, right)
anaglified = cutImage(anaglified)
cv.imshow('anaglif', anaglified)
cv.imwrite('result.jpg', anaglified)
cv.waitKey(0)