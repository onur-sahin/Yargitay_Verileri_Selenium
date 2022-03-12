
import pandas
from numpy import average
from PIL import Image
def to_grayscale(arr):
    "If arr is a color image (3D array), convert it to grayscale (2D array)."
    if len(arr.shape) == 3:
        return average(arr, -1)  # average over the last axis (color channels)
    else:
        return arr


file1 = '''C:\\Users\\asus\\Documents\\GitHub\\Yargitay_Verileri_Selenium\\captcha_images\\1.png'''
file2 = '''C:\\Users\\asus\Documents\\GitHub\\Yargitay_Verileri_Selenium\\captcha_images\\2.png'''
img1 = Image.open(file1)
# read images as 2D arrays (convert to grayscale for simplicity)
#img1 = to_grayscale(Image.open(file1).astype(float))
#img2 = to_grayscale(Image.open(file2).astype(float))
# compare

print(img1)






