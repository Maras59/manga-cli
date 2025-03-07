import sys
from PIL import Image, ImageEnhance
import numpy as np

IMG_WIDTH = 100  
ASCII_POOL = " `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"

def conv_image(fname):
    try:
        img = Image.open(fname)

        img = img.convert('L')

        aspect_ratio = img.height / (img.width * 2.5)
        new_height = int(IMG_WIDTH * aspect_ratio)
        img = img.resize((IMG_WIDTH, new_height), Image.LANCZOS)

        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)

        sharpen = ImageEnhance.Sharpness(img)
        img = sharpen.enhance(2.0)

        img.save('python/tmp/output.bmp', format='BMP')

        img_array = np.array(img)
        return img_array

    except FileNotFoundError:
        print(f'Error: File "{fname}" not found.', flush=True)
        return None

def normalize_intensity(array):
    min_val = array.min()
    max_val = array.max()
    img_array = ((array - min_val) / (max_val - min_val)) * (len(ASCII_POOL) - 1)
    img_array = img_array.astype(np.uint8)
    return img_array

def draw(array):
    for x in array:
        for y in x:
            print(ASCII_POOL[y], end='')
        print()
    sys.stdout.flush()

image_array = conv_image('python/tmp/image3.png')
if image_array is None:
    sys.exit(1)

image_array = normalize_intensity(image_array)
draw(image_array)
