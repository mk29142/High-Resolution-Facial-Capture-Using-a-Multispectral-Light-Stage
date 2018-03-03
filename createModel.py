import PhotoScan
import os

path = os.path.dirname(os.path.abspath(__file__)) + "/"
doc = PhotoScan.app.document
chunk = doc.addChunk()

photos = []

for i in range(1,7):
    photos.append(path + "card{}.JPG".format(i))

chunk.addPhotos(photos)
for frame in chunk.frames:
    frame.matchPhotos(accuracy=PhotoScan.HighAccuracy)
chunk.alignCameras()

doc.save(path=path+"test.psz", chunks= [doc.chunk])

# print("Hello World") 

