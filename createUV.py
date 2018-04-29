import PIL
from PIL import Image
import math
import numpy as np
from numpy import array

def createUVSpace():

    images = []

    uvImage = np.zeros([4096, 4096, 3],dtype=np.uint8)
    uvImage.fill(0)

    prefix = "./diffuseNormals/"

    names = [prefix + "diffuseNormal{}".format(str(name)) + ".png" for name in range(1, 11)]

    for i in names:
        img = Image.open(i)
        arr = array(img)
        images.append(arr.astype('float64'))

    height, width, _ = images[0].shape
    for image in images:
        for h in range(height):
            for w in range(width):
                x = image[h][w][0]
                y = image[h][w][1]
                z = image[h][w][2]

                counter = 0

                if z == 0.0:
                    counter += 1
                    continue
                if x == 127.0 and y == 127.0 and z == 127.0:
                    continue

                u = math.atan2(x,z)
                u = u/math.pi
                u = u + 1
                u = u / 2
                u = u * 4095
                u = int(u)

                v = (y / 255) * 4095
                v = int(v)
                # print(u, v, x, y, z, math.atan2(x,z))

                uvImage[u][v][0] = int(x)
                uvImage[u][v][1] = int(y)
                uvImage[u][v][2] = int(z)


    print(counter)
    
    im = Image.fromarray(uvImage.astype('uint8'))
    im.save("uv.png")

if __name__ == "__main__":
    createUVSpace()