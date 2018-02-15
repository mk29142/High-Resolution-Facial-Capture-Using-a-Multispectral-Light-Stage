import PIL
import numpy as np
from PIL import Image
from numpy import array

def calculateMixedNormals():
    images = []

    names = ["X.jpg", "XN.jpg", "Y.jpg", "YN.jpg", "Z.jpg", "ZN.jpg"]

    for i in names:
        img = Image.open(i)
        arr = array(img)
        images.append(arr.astype('float64'))

    # print(len(images))

    height, width, _ = images[0].shape

    N_x = (images[0] - images[1]) / 255
    N_y = (images[2] - images[3]) / 255
    N_z = (images[4] - images[5]) / 255

    encodedImage = np.empty_like(N_x).astype('float64')

    # print(height, width)

    encodedImage[..., 0] = N_x[..., 2]
    encodedImage[..., 1] = N_y[..., 2]
    encodedImage[..., 2] = N_z[..., 2]

    for h in range(height):
        for w in range(width):
            red = encodedImage[h][w][0]
            green = encodedImage[h][w][1]
            blue = encodedImage[h][w][2]

            denom = np.power(red, 2) + np.power(green, 2) + np.power(blue, 2)

            if denom == 0.0:
                normalisingFactor = 1.0
            else:
                normalisingFactor = 1.0 / np.sqrt(denom)

            encodedImage[h][w][0] *= normalisingFactor
            encodedImage[h][w][1] *= normalisingFactor
            encodedImage[h][w][2] *= normalisingFactor


    encodedImage = (encodedImage + 1.0) / 2.0

    encodedImage *= 255.0

    # print(encodedImage.shape)

    im = Image.fromarray(encodedImage.astype('uint8'))
    im.save("encodedImage.jpg")






if __name__ == "__main__":
    calculateMixedNormals()