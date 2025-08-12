from PIL import Image

print("Image is:", Image)
print("Image.open attribute:", getattr(Image, 'open', None))
