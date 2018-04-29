import PIL
from PIL import Image
import math
import numpy as np
from numpy import array
import time
import xml.etree.ElementTree as ET
from toolz.dicttoolz import valmap

start_time = time.time()

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

def createUVSpace2(pathToPLY, pathToTexture):

    uvImage = np.zeros([1024, 1024, 3],dtype=np.uint8)
    uvImage.fill(0)

    with open(pathToPLY) as f:
        numberOfVerticies = 0
        numberOfFaces = 0

        while(True):
            line = f.readline()
            if "end_header" in line:
                break
            if "element vertex" in line:
                numberOfVerticies = int(line.split(" ")[-1])
            if "element face" in line:
                numberOfFaces = int(line.split(" ")[-1])
        
        verticies = []

        for i in range(numberOfVerticies):
            coords = f.readline().replace(" \n", "").split(" ")
            coords = map(float, coords)
            # coords = np.dot(rotationMatrix, coords).tolist()[0]
            verticies.append(coords)

        indexToUV = {}

        # for i in range(numberOfFaces):
        while(True):
            line = f.readline()
            if line == '':
                break
            line = line.split(" ")
            indexes = line[1:4]
            indexes = map(int, indexes)
            UVCoords = line[5:-1]
            UVCoords = map(float, UVCoords)
            for j in range(0, 3):
                index = str(indexes[j])
                indexToUV[index] = [UVCoords[j*2], UVCoords[j*2 + 1]]

        textureImage = array(Image.open(pathToTexture))
        us = []
        vs = []

        keys = indexToUV.keys()
        coords = []

        for key in keys:
            vertex = int(key)
            x = verticies[vertex][0]
            y = verticies[vertex][1]
            z = verticies[vertex][2]
            coords.append(indexToUV[key])

            u = np.arctan(x/z)
            us.append(u)

            v = y
            vs.append(v)

        minU = min(us)*-1

        newUs = map(lambda x: x + minU, us)
        maxU = max(newUs)
        newUs = map(lambda x: x / maxU, newUs)
        newUs = map(lambda x: int(x*1023), newUs)

        minV = min(vs)*-1

        newVs = map(lambda x: x + minV, vs)
        maxV = max(newVs)
        newVs = map(lambda x: x / maxV, newVs)
        newVs = map(lambda x: int(x*1023), newVs)

        # # print(len(us), len(newVs))
        newCoords = zip(newUs, newVs, coords)

        for coord in newCoords:
            # print(coord)
            u = coord[0]
            v = coord[1]
            
            tU = coord[2][0] * 4096
            tV = coord[2][1] * 4096

            R = textureImage[int(tV)][int(tU)][0]
            G = textureImage[int(tV)][int(tU)][1]
            B = textureImage[int(tV)][int(tU)][2]

            uvImage[u][v][0] = 255
            uvImage[u][v][1] = 255
            uvImage[u][v][2] = 255

        im = Image.fromarray(uvImage.astype('uint8'))
        im.save("uv2.png")

if __name__ == "__main__":
    # createUVSpace()
    createUVSpace2("lowresForUV.ply", "textureForUV.png")

    print("--- %s seconds ---" % (time.time() - start_time))
