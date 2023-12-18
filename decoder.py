import numpy as np
import gzip
from PIL import Image

def to_bytes(data):
    bytes = data.flatten().tobytes() # Convert the data to bytes
    bytes = gzip.decompress(bytes) # Decompress the bytes

    # Separate the filename from the rest of the data
    filename, bytes = bytes.split(b'\x00', 1)
    filename = filename.decode()

    return filename, bytes

def decode_image(image_path):
    img = Image.open(image_path)
    data = np.array(img)
    filename, bytes_output = to_bytes(data)
    return filename,bytes_output
