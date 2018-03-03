import PhotoScan
import os

PhotoScan.gpu_mask = 1  #GPU devices binary mask
PhotoScan.cpu_enable = 2  #CPU cores inactive

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

chunk.buildDepthMaps(quality = PhotoScan.UltraQuality, filter = PhotoScan.AggressiveFiltering)
chunk.buildDenseCloud()
chunk.buildModel(surface = PhotoScan.Arbitrary, interpolation = PhotoScan.EnabledInterpolation, face_count = 1000000, source = PhotoScan.DataSource.DenseCloudData)

doc.save(path=path+"test.psz", chunks= [doc.chunk])


