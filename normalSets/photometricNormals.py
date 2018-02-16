import PIL
import numpy as np
from PIL import Image
from numpy import array
from sklearn.preprocessing import normalize
import time
start_time = time.time()

def calculateMixedNormals():
    images = []

    names = ["X.jpg", "XN.jpg", "Y.jpg", "YN.jpg", "Z.jpg", "ZN.jpg"]

    for i in names:
        img = Image.open(i)
        arr = array(img)
        images.append(arr.astype('float64'))

    height, width, _ = images[0].shape

    N_x = (images[0] - images[1]) / 255
    N_y = (images[2] - images[3]) / 255
    N_z = (images[4] - images[5]) / 255

    encodedImage = np.empty_like(N_x).astype('float64')

    encodedImage[..., 0] = N_x[..., 2]
    encodedImage[..., 1] = N_y[..., 2]
    encodedImage[..., 2] = N_z[..., 2]

    for h in range(height):
        normalize(encodedImage[h], copy=False)

    encodedImage = (encodedImage + 1.0) / 2.0

    encodedImage *= 255.0

    im = Image.fromarray(encodedImage.astype('uint8'))
    im.save("encodedImage4.jpg")






if __name__ == "__main__":
    calculateMixedNormals()
    print("--- %s seconds ---" % (time.time() - start_time))