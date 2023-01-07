// MathLibrary.cpp : Defines the exported functions for the DLL.
#include "pch.h" // use stdafx.h in Visual Studio 2017 and earlier
#include <utility>
#include <limits.h>
#include "AnaglyphLib.h"


void Calculate(int* pixelValues)
{
    for (int i = 0; i < 12; i+=3)
    {
        pixelValues[i + 2] = pixelValues[i] * 0.114 + pixelValues[i + 1] * 0.587 + pixelValues[i + 2] * 0.299;
        pixelValues[i] = pixelValues[i+ 12] * 0.114 + pixelValues[i+ 12 + 1] * 0.587 + pixelValues[i + 12 + 2] * 0.299;
        pixelValues[i + 1] = pixelValues[i];
    }
    
}