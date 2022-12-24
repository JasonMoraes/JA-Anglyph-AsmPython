import numpy as np
import cv2 as cv
import ctypes as ct


class tabASM(ct.Structure):
    _fields_ = [("B", ct.POINTER(ct.c_int)), ("G", ct.POINTER(ct.c_int)), ("R", ct.POINTER(ct.c_int))]


def anglifyASM(left, right):
    height = left.shape[0]
    width = left.shape[1]
    returnedImage = np.zeros([height, width, 3], dtype='uint8')
    asmDll = ct.WinDLL("C:\\Users\\blaze\\PycharmProjects\\ctypes\\DllAsm.dll")
    for i in range(0, width*height, 4):

        #Get 4 pixels from left image
        pixL = getPixel(left, i)
        pixL2 = getPixel(left, i + 1)
        pixL3 = getPixel(left, i + 2)
        pixL4 = getPixel(left, i + 3)

        #Get 4 pixels from right image
        pixR = getPixel(right, i)
        pixR2 = getPixel(right, i + 1)
        pixR3 = getPixel(right, i + 2)
        pixR4 = getPixel(right, i + 3)

        #Create 3 arrays off left BGR values
        pyLarrB = [pixL[0], pixL2[0], pixL3[0], pixL4[0]]
        pyLarrG = [pixL[1], pixL2[1], pixL3[1], pixL4[1]]
        pyLarrR = [pixL[2], pixL2[2], pixL3[2], pixL4[2]]

        #Create 3 arrays off right BGR values
        pyRarrB = [pixR[0], pixR2[0], pixR3[0], pixR4[0]]
        pyRarrG = [pixR[1], pixR2[1], pixR3[1], pixR4[1]]
        pyRarrR = [pixR[2], pixR2[2], pixR3[2], pixR4[2]]

        seq = ct.c_int * len(pyLarrB)
        arrLB = seq(*pyLarrB)
        arrLG = seq(*pyLarrG)
        arrLR = seq(*pyLarrR)

        arrRB = seq(*pyRarrB)
        arrRG = seq(*pyRarrG)
        arrRR = seq(*pyRarrR)
        arrLeftStruct= tabASM(arrLB,arrLG,arrLR)
        arrRightStruct = tabASM(arrRB,arrRG,arrRR)
        asmDll.Calculate(arrLeftStruct)
        asmDll.Calculate(arrRightStruct)

        parsedBGArray = ct.cast(arrLG, ct.POINTER(ct.c_long * 12))
        parsedRArray = ct.cast(arrLB, ct.POINTER(ct.c_long * 12))
        pythonBGList = parsedBGArray.contents[:]
        pythonRList = parsedRArray.contents[:]

        rpix = getPixel(returnedImage, i)
        rpix2 = getPixel(returnedImage, i + 1)
        rpix3 = getPixel(returnedImage, i + 2)
        rpix4 = getPixel(returnedImage, i + 3)

        rpix[0] = pythonBGList[0]
        rpix[1] = pythonBGList[0]
        rpix[2] = pythonRList[0]
        #
        rpix2[0] = pythonBGList[1]
        rpix2[1] = pythonBGList[1]
        rpix2[2] = pythonRList[1]
        #
        rpix3[0] = pythonBGList[2]
        rpix3[1] = pythonBGList[2]
        rpix3[2] = pythonRList[2]
        #
        rpix4[0] = pythonBGList[3]
        rpix4[1] = pythonBGList[3]
        rpix4[2] = pythonRList[3]



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
    returnedImage = np.zeros([height, width, 3], dtype=ct.c_int)
    for i in range(0, height):
        for j in range(0, width):
            returnedImage[i][j][2] = img[i][j + 5][2]
            returnedImage[i][j][1] = img[i][j + 5][1]
            returnedImage[i][j][0] = img[i][j + 5][0]
    return returnedImage

def getPixel(img, idx):
    height = img.shape[0]
    width = img.shape[1]
    row= int(idx/width)
    col= idx % width
    return img[row][col]

img = cv.imread('sample.jpg')
left =  moveTenToLeft(img)
right = moveTenToRight(img)
anaglified = anglifyASM(left,right)

cv.imshow('anglif', anaglified)
cv.waitKey(0)
