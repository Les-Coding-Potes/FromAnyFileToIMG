from PIL import Image
import numpy as np
import gzip
import argparse
import os

class OutputType:
    Bitmap = 0
    Video = 1

def to_bitmap(bytes, filename):
    # Ajoutez le nom du fichier aux bytes
    bytes = filename.encode() + b'\x00' + bytes

    # On compresse les bytes au debut 
    bytes = gzip.compress(bytes)

    # On calcult la taille de l'image en fonction de la taille des bytes
    required_size = len(bytes) + 4  # +4 for the end of data marker
    required_width = int(np.ceil(np.sqrt(required_size / 4))) 
    required_height = required_width

    size = required_width * required_height * 4  # 4 bytes per pixel (RGBA)

    if len(bytes) < size:
        bytes += b'\x00' * (size - len(bytes))  # Arrivé a la fin on rempli avec des 0

    data = np.frombuffer(bytes, dtype=np.uint8) # On converti les bytes en array numpy pour optimiser
    image = np.reshape(data, (required_height, required_width, 4)) # On reshape l'array pour avoir une image
    image = Image.fromarray(image, 'RGBA')

    return image

parser = argparse.ArgumentParser(description='Process some files.')
parser.add_argument('file_path', type=str, help='The path to the input file')
parser.add_argument('output_dir', type=str, help='The directory to write the output image')

args = parser.parse_args()

try:
    with open(args.file_path, "rb") as file:
        file_bytes_input = file.read()
        
        # Get the filename from the file path
        filename = os.path.basename(args.file_path)
        
        bitmap_output = to_bitmap(file_bytes_input, filename)
        
        # Use the same filename but with .png extension for the output image
        output_image_path = os.path.join(args.output_dir, os.path.splitext(filename)[0] + '.png')
        bitmap_output.save(output_image_path)

except IOError as e:
    raise Exception(f"Error: {e}")



#python encoder.py "E:\New folder\test.json" "E:\New folder"