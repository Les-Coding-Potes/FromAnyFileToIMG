from PIL import Image
import numpy as np
import gzip

class OutputType:
    Bitmap = 0
    Video = 1

def to_bitmap(bytes):
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
    
def to_bytes(bitmap):
    data = np.array(bitmap)
    bytes = data.flatten().tobytes() # On converti l'image en bytes
    bytes = gzip.decompress(bytes) # Une fois toutes les données récupérées on décompresse les bytes

    return bytes

if __name__ == "__main__":
    file_path = r"E:\New folder\test.json"
    output_file_path = r"E:\New folder\output_file.json"
    image_path = r"E:\New folder\output_image.png"

    #Les methodes to_bitmap et to_bytes sont independente mais pour du test on les utilise ensemble
    try:
        with open(file_path, "rb") as file:
            file_bytes_input = file.read()
            
            bitmap_output = to_bitmap(file_bytes_input)
            bitmap_output.save(image_path, "PNG")

            bytes_output = to_bytes(bitmap_output)
            with open(output_file_path, "wb") as output_file:
                output_file.write(bytes_output)

    except IOError as e:
        raise Exception(f"Error: {e}")
