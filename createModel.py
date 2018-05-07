import PhotoScan
import os

PhotoScan.gpu_mask = 1  #GPU devices binary mask
PhotoScan.cpu_enable = True

path = os.path.dirname(os.path.abspath(__file__)) + "/"

def createAndSaveModel(filename):
    doc = PhotoScan.app.document
    chunk = doc.addChunk()

    photos = []

    for i in range(1, 11):
        photos.append(path + "card{}.JPG".format(i))

    chunk.addPhotos(photos) 

    # align cameras, first pass
    for frame in chunk.frames:
        frame.matchPhotos(accuracy=PhotoScan.HighAccuracy)
    chunk.alignCameras()

    # align all unaligned cameras not done in first pass
    for camera in doc.chunk.cameras:
        if not camera.transform:
            doc.chunk.alignCameras([camera])

    chunk.optimizeCameras(adaptive_fitting=True)

    chunk.buildDepthMaps(quality = PhotoScan.UltraQuality, filter = PhotoScan.AggressiveFiltering)
    chunk.buildDenseCloud()
    chunk.buildModel(surface = PhotoScan.Arbitrary, interpolation = PhotoScan.EnabledInterpolation, face_count = PhotoScan.FaceCount.MediumFaceCount, source = PhotoScan.DataSource.DenseCloudData)

    chunk.exportCameras("{}bundlerTest.out".format(path), PhotoScan.CamerasFormat.CamerasFormatBundler)
    chunk.exportCameras("{}agisoftXMLTest.xml".format(path), PhotoScan.CamerasFormat.CamerasFormatXML)
    chunk.exportCameras("{}blocksExchangeTest.xml".format(path), PhotoScan.CamerasFormat.CamerasFormatBlocksExchange)
    chunk.exportModel("{}modelExportTest.obj".format(path), format=PhotoScan.ModelFormat.ModelFormatOBJ)

    doc.save(path=path+filename, chunks= [doc.chunk])


if __name__ == "__main__":
    createAndSaveModel("test.psz")
