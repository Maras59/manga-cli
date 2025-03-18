import sys
from PIL import Image, ImageEnhance
import numpy as np

ASCII_POOL = " `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"

def conv_image(fname, max_height, max_width):

    try:
        img = Image.open(fname)

        img = img.convert('L')

        orig_width, orig_height = img.size

        aspect_ratio = img.height / (img.width * 2.5)

        if orig_width > orig_height:
            # Scale based on width
            new_width = min(orig_width, max_width)
            new_height = int(new_width * aspect_ratio)
            if new_height > max_height:
                # If the scaled height exceeds max_height, scale based on height instead
                new_height = min(orig_height, max_height)
                new_width = int(new_height / aspect_ratio)
        else:
            # Scale based on height
            new_height = min(orig_height, max_height)
            new_width = int(new_height / aspect_ratio)
            if new_width > max_width:
                # If the scaled width exceeds max_width, scale based on width instead
                new_width = min(orig_width, max_width)
                new_height = int(new_width * aspect_ratio)

        img = img.resize((new_width, new_height), Image.LANCZOS)

        # enhancer = ImageEnhance.Contrast(img)
        # img = enhancer.enhance(2.0)

        # sharpen = ImageEnhance.Sharpness(img)
        # img = sharpen.enhance(2.0)

        img.save('pyscripts/tmp/output.bmp', format='BMP')

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

width = int(sys.argv[1])
height = int(sys.argv[2])
image_array = conv_image('pyscripts/tmp/image5.png', width, height)

if image_array is None:
    sys.exit(1)

image_array = normalize_intensity(image_array)
draw(image_array)
