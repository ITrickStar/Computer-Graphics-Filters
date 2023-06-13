// Copyright 2021 Miheev Ivan

#include <opencv2/core/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/imgproc.hpp>

#include "./vertical_gauss.h"

using namespace cv;


int main(int argc, char** argv) {
  MPI_Init(&argc, &argv);
  int rank;
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);

  Mat mat = imread("input.jpg", IMREAD_GRAYSCALE);

  std::vector<uchar> arr;
  arr.assign(mat.data, mat.data + mat.total());

  int* image = nullptr;
  const int width = mat.cols, height = mat.rows;

  if (rank == 0) {
    imshow("Original", mat);
    image = new int[width * height];
    int counter = 0;
    for (auto elem : arr) {
      image[counter] = elem;
      counter++;
    };
  }

  int* new_image_parallel = getParallelGauss(image, width, height);

  if (rank == 0) {
    Mat new_mat = Mat::zeros(height - 2, width - 2, CV_8UC1);
    for (int r = 0; r < mat.rows - 2; r++) {
      for (int c = 0; c < mat.cols - 2; c++) {
        new_mat.at<uchar>(r, c) =
            new_image_parallel[c + r * (width - 2)];
      }
    }

    imshow("Parallel", new_mat);
    waitKey();
    int* reference_new_image = getSequentialGauss(image, width, height);
  }
  MPI_Finalize();
}
