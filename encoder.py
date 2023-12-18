from PIL import Image
import numpy as np
import gzip
from enum import Enum

def to_bitmap(bytes, filename):
    # Ajoute le nom du fichier aux bytes
    bytes = filename.encode() + b'\x00' + bytes
 
    # On compresse les bytes au debut 
    bytes = gzip.compress(bytes)
 
    # On calcule la taille de l'image en fonction de la taille des bytes
    required_size = len(bytes) + 4  # +4 for the end of data marker
    required_width = int(np.ceil(np.sqrt(required_size / 4)))
    required_height = required_width

    size = required_width * required_height * 4  # 4 bytes per pixel (RGBA)

    if len(bytes) < size:
        bytes += b'\x00' * (size - len(bytes))  # Arrivé à la fin, on remplit avec des 0

    data = np.frombuffer(bytes, dtype=np.uint8) # On convertit les bytes en array numpy pour optimiser
    image = np.reshape(data, (required_height, required_width, 4)) # On reshape l'array pour avoir une image
    image = Image.fromarray(image, 'RGBA')

    return image
