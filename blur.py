import PIL
from PIL import Image
from PIL import ImageFilter

specular = Image.open("blenderTexture.png")
blurredSpecular = specular.filter(PIL.ImageFilter.GaussianBlur(radius=1))

blurredSpecular.save("blenderTexture.png", "PNG")