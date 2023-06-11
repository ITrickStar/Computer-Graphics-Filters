#main.py

from functions import *
import glob

# READ IMAGE
folder_path = r"D:\Works\Python\Fourier\stripes"
images = glob.glob(folder_path + '/' + '*.png')

if images is None:
    sys.exit("Could not read the images")

for name in images:
    img = np.float32(cv.imread(name, 0))
    
    #im1 = GaussianLPF(img)
    #showDFFT(img, name)
    ntch_img = notch_filter(img)
    #cv.imwrite ("notch2_" +  name[len(folder_path)+1:], ntch_img)
# =============================================================================
#     plt.figure(figsize=(10,10))
#     plt.imshow(ntch_img, 'Greys')
#     plt.axis('off')
#     plt.show()
# =============================================================================
    #plt.savefig("notch_" +  name[len(folder_path)+1:])


# =============================================================================
#     fshift = DFFTnp(img)
#     plt.imshow(fshift)
# =============================================================================
