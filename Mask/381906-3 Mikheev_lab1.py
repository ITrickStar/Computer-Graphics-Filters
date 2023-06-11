# Libraries and functions
import numpy as np
import cv2
import sys

def CalcOfDamageAndNonDamage (image) :
    kernel = cv2.getStructuringElement (cv2.MORPH_ELLIPSE, (7, 7))
    image_erode = cv2.erode (image, kernel)

    hsv_img = cv2.cvtColor(image_erode, cv2.COLOR_BGR2HSV)

    markers = np.zeros((image.shape[0], image.shape[1]), dtype = "int32")
    markers [90:140, 90:140] = 3
    markers [230:255, 0:20] = 1
    markers [230:255, 0:100] = 1
    markers [0:20, 0:20] = 1
    markers [0:20, 220:255] = 1
    markers [230:255, 230:255] = 1
    
    leafs_area_BGR = cv2.watershed (image_erode, markers)

    healthy_part = cv2.inRange(hsv_img, (40, 20, 20), (90, 255, 255))
    shadow_part = cv2.inRange(hsv_img, (0,0,0), (180, 180, 40))
    ill_part = leafs_area_BGR - healthy_part - shadow_part
    
    mask = np.zeros_like(image, np.uint8)
    mask [leafs_area_BGR > 1] = (255, 55, 255)
    mask [ill_part > 1] = (0 ,0, 255)
    mask [shadow_part > 1] = (0, 0, 0)
    
    return mask


# Main
img = cv2.imread ("D:\\Downloads\\Images\\1.jpg")
if img is None:
    sys.exit("Could not read the image")

_msk = CalcOfDamageAndNonDamage(img)

bil = cv2.bilateralFilter (img, 15, 75, 75)
b_msk = CalcOfDamageAndNonDamage(bil)
    
nlm = cv2.fastNlMeansDenoisingColored (img, None, 10, 10, 7, 21)
n_msk = CalcOfDamageAndNonDamage(nlm)

med = cv2.medianBlur(img, 5)
m_msk = CalcOfDamageAndNonDamage(med)

# Filter
filtered = med
msk = m_msk
dif = b_msk - m_msk

cv2.imshow ("Original", img)
cv2.imshow ("Filter", filtered)
cv2.imshow ("Mask", msk)
cv2.imshow ("Difference", dif)

k = cv2.waitKey(0)

if k == ord ('s') :
    cv2.imwrite ("msk_1_dif.png", dif)

cv2.destroyAllWindows()