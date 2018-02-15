import PIL
from PIL import Image
from numpy import array

f = []

names = ["X.jpg", "XN.jpg", "Y.jpg", "YN.jpg", "Z.jpg", "ZN.jpg"]

for i in names:
    img = Image.open(i)
    arr = array(img)
    f.append(arr)

print(len(f))