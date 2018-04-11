import PIL
import numpy as np
from PIL import Image
from numpy import array
from sklearn.preprocessing import normalize
import time
import xml.etree.ElementTree as ET

start_time = time.time()

NumberOfCameras = 0

def calculateMixedNormals():

    for card in range(1, 7):

        images = []

        prefix = "./normalSets6/card" + str(card) + "/"

        names = ["1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg", "6.jpg"]

        names = [prefix + name for name in names]

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


        # only for visualising
        encodedImage = (encodedImage + 1.0) / 2.0
        encodedImage *= 255.0

        im = Image.fromarray(encodedImage.astype('uint8'))
        im.save("encoded{}.jpg".format(card))

def calculateDiffuseNormals():

    for card in range(1, 11):

        images = []

        prefix = "./normalSets10/card{}/".format(card)

        names = [prefix + str(name) + ".JPG" for name in range(3, 16, 2)]
        names.remove(prefix + "11.JPG")

        print(names)

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

        # only for visualising
        encodedImage = (encodedImage + 1.0) / 2.0
        encodedImage *= 255.0

        im = Image.fromarray(encodedImage.astype('uint8'))
        im.save("diffuseNormal{}.jpg".format(card))

def calculateSpecularNormals():

    images = []

    card = 1

    prefix = "./normalSets10/card{}/".format(card)

    xGradients = [prefix + str(name) + ".JPG" for name in range(3, 7)]
    yGradients = [prefix + str(name) + ".JPG" for name in range(7, 11)]
    zGradients = [prefix + str(name) + ".JPG" for name in range(13, 17)]

    names = xGradients + yGradients + zGradients

    for i in names:
            img = Image.open(i)
            arr = array(img)
            images.append(arr.astype('float64'))

    height, width, _ = images[0].shape

    xImages = images[:4]
    yImages = images[4:8]
    zImages = images[8:]

    specularXImages = [xImages[1] - xImages[0], xImages[3] - xImages[2]]
    specularYImages = [yImages[1] - yImages[0], yImages[3] - yImages[2]]
    specularZImages = [zImages[1] - zImages[0], zImages[3] - zImages[2]]

    images = specularXImages + specularYImages + specularZImages


def getPhotoXMLBlock(path):
    tree = ET.parse(path)
    root = tree.getroot()
    block = root.find('Block')
    photoGroups = block.find('Photogroups').findall('Photogroup')
    photos = map(lambda photogroup: photogroup.findall('Photo') , photoGroups)
    photos = reduce(lambda x,y: x+y, photos)
    return photos

def getCameraName(photoTag):
    imagePath = photoTag.find('ImagePath').text
    name = imagePath.split('/')[-1].split('.')[0]
    return name

def getTranslationVectorPerCamera(path):

    photos = getPhotoXMLBlock(path)
    NumberOfCameras = len(photos)

    vectorPerCamera = {}

    for photo in photos:
        name = getCameraName(photo)

        center = photo.find('Pose').find('Center')
        
        #may need to negate coord value for meshlab project
        coords = map(lambda axis: float(axis.text), center)
        vectorPerCamera[name] = coords
    
    return vectorPerCamera

def getRotationMatrixPerCamera(path):
    with open(path) as f:
        f.readline()
        f.readline()
        f.readline()

        rotationMatricPerCamera = {}

        for i in range(1,NumberOfCameras+1):
            card = "card{}".format(i)

            matrix = ""
            for j in range(3):
                matrix += f.readline()
                matrix += "0 "
            
            f.readline()
            f.readline()
            matrix += "0 0 0 1"

            rotationMatricPerCamera[card] = matrix
        
    return rotationMatricPerCamera



if __name__ == "__main__":
    # calculateMixedNormals()
    # calculateDiffuseNormals()
    # calculateSpecularNormals()
    getTranslationVectorPerCamera('blocksExchangeForSpecular.xml')
    getRotationMatrixPerCamera('bundler.out')
    print("--- %s seconds ---" % (time.time() - start_time))