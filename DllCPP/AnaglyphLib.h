// MathLibrary.h - Contains declarations of math functions
#pragma once

#ifdef ANAGLYPHLIB_EXPORTS
#define ANAGLYPHLIB_API __declspec(dllexport)
#else
#define ANAGLYPHLIB_API __declspec(dllimport)
#endif

extern "C" ANAGLYPHLIB_API void Calculate(int* pixelValues);
