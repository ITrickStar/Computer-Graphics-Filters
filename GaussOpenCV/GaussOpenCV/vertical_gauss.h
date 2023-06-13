// Copyright 2021 Mikheyev Ivan
#ifndef MODULES_TASK_3_MIHEEV_I_VERTICAL_GAUSS_VERTICAL_GAUSS_H_
#define MODULES_TASK_3_MIHEEV_I_VERTICAL_GAUSS_VERTICAL_GAUSS_H_

#include <mpi.h>

int* getRandomImage(int width, int height);
int* getSequentialGauss(const int* image, int width, int height);
int* getParallelGauss(const int* image, int width, int height);

#endif  // MODULES_TASK_3_MIHEEV_I_VERTICAL_GAUSS_VERTICAL_GAUSS_H_
