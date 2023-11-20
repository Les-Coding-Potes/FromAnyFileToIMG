import numpy as np
import gzip
from PIL import Image
import argparse
import os

def to_bytes(bitmap):
    data = np.array(bitmap)
    bytes = data.flatten().tobytes() # On converti l'image en bytes
    bytes = gzip.decompress(bytes) # Une fois toutes les données récupérées on décompresse les bytes

    # Séparez le nom du fichier du reste des données
    filename, bytes = bytes.split(b'\x00', 1)
    filename = filename.decode()

    return filename, bytes

parser = argparse.ArgumentParser(description='Process some images.')
parser.add_argument('image_path', type=str, help='The path to the image file')
parser.add_argument('output_dir', type=str, help='The directory to write the output file')

args = parser.parse_args()

# Ouvrez l'image avec PIL et convertissez-la en bitmap
img = Image.open(args.image_path)
bitmap = np.array(img)

# Appliquez la fonction to_bytes à l'image
filename, bytes_output = to_bytes(bitmap)

# Affichez le nom du fichier
print(f"Filename: {filename}")

# Construisez le chemin du fichier de sortie
output_file_path = os.path.join(args.output_dir, filename)

try:
    with open(output_file_path, "wb") as output_file:
        output_file.write(bytes_output)

except IOError as e:
    raise Exception(f"Error: {e}")


#python decoder.py "E:\New folder\output_image.png" "E:\New folder"