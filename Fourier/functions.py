#functions.py

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def showDFFT(img, name) :

    fshift = DFFTnp(img)
    magnitude = 20*np.log(np.abs(fshift))
    
    plt.subplot(121), plt.imshow(img, 'Greys', vmin = 0 ,vmax = 255)
    plt.title ('Input Image'), plt.xticks([]), plt.yticks([])

    s_min = magnitude.min()
    s_max = magnitude.max()
    if(s_min == s_max):
         plt.subplot(122), plt.imshow(magnitude, 'Greys', vmin = 0 , vmax = 255)
    else:
        plt.subplot(122), plt.imshow(magnitude , 'Greys')

    plt.title ('Magnitude Spectrum'), plt.xticks ([]), plt.yticks ([])
    plt.show()

def DFFTnp( img ) :
    #f = cv.dft(np.float32(img),flags = cv.DFT_COMPLEX_OUTPUT)
    f=np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    return fshift

def reverseDFFTnp (dfft) :
    recovered_shift_img = np.fft.ifftshift(dfft)
    recovered_image = np.fft.ifft2(recovered_shift_img)
    reverse_image=np.abs(recovered_image)
    return reverse_image

def notch_filter(img):
    img = cv.GaussianBlur(img,(5,5),1)
    
    f = DFFTnp(img)
    
    plt.figure(figsize=(6.66,10))
    plt.imshow((20*np.log10(0.1 + f)).astype(int), cmap=plt.cm.gray)
    plt.show()
    
    img = np.abs(img)
    q = 0.95
    
    mag = np.abs(f)
    print('mean =', np.quantile(mag,q), q)
    mag_q = np.quantile(mag, q)
    hazard = 5
    center = 5

    dmz_x=[int(img.shape[0]/2 - img.shape[0]/center +1 ),int(img.shape[0]/2 + img.shape[0]/center + 1)]
    dmz_y=[int(img.shape[1]/2 - img.shape[1]/center +1 ),int(img.shape[1]/2 + img.shape[1]/center + 1)]
    x_len,y_len=f.shape
    for x in range(0,x_len):
            for y in range(0,y_len):
                if np.abs(f[x][y])>mag_q:
                    if dmz_x[0]< x <dmz_x[1] and dmz_y[0]< y <dmz_y[1]:
                        continue
                    else:
                        f[max(0,x-hazard):min(x+hazard,x_len), max(0,y-hazard):min(y+hazard,y_len)]=0

    
    img_back = reverseDFFTnp(f)
    #img_back = cv.magnitude(img_back[:,:,0],img_back[:,:,1])
    
    plt.figure(figsize=(6.66,10))
    plt.imshow((20*np.log10(0.1 + f)).astype(int), cmap=plt.cm.gray)
    plt.show()

    plt.figure(figsize=(10,10))
    plt.imshow(img_back, cmap='gray')
    plt.axis('off')
    plt.show()

    return img_back

def GaussianLPF(img):
    # BLUR
    ksize = 21
    kernel = np.zeros(img.shape )
    blur = cv.getGaussianKernel (ksize, 5)
    blur = np.matmul (blur, np.transpose(blur))
    kernel [0:ksize, 0:ksize] = blur
    fkshift = DFFTnp(kernel)
    fshift = DFFTnp(img)
    mult = np.multiply (fshift, fkshift)
    reverse_image = reverseDFFTnp(mult)
# =============================================================================
#     plt.imshow (abs(reverse_image), cmap = 'gray' )
#     plt.title ( "Sobel" )
#     plt.show()
# =============================================================================
    return reverse_image

def Sobel(img):
    ksize = 3
    kernel = np.zeros(img.shape)
    sobel_v = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
    sobel_h = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    kernel [0:ksize, 0:ksize] = sobel_h

    fkshift = DFFTnp(kernel)
    fshift = DFFTnp(img)
    mult = np.multiply(fshift, fkshift)
    reverse_image = reverseDFFTnp(mult)
# =============================================================================
#     plt.imshow (abs(reverse_image), cmap = 'gray' )
#     plt.title ( "Sobel" )
#     plt.show()
# =============================================================================
    return reverse_image

# =============================================================================
# folder_path = r"D:\Works\Python\Fourier\images/"
# images = glob.glob(folder_path + '*.png')
# for name in images:
#     img = np.float32(cv.imread(name, 0))
#     f = np.fft.fft2 ( img )
#     fshift = np.fft.fftshift ( f )
#     showDFFT(img, fshift, name)
# 
# =============================================================================
