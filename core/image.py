import numpy as np
from PIL import Image
import os

def split(img_input, splits, splits_dir):
    input_image = Image.open(img_input)
    image = np.asarray(input_image)
    (row, column, depth) = image.shape
    shares = np.random.randint(0, 256, size=(row, column, depth, splits))

    shares[:,:,:,-1] = image.copy()
    for i in range(splits-1):
        shares[:,:,:,-1] = shares[:,:,:,-1] ^ shares[:,:,:,i]

    part_paths = []
    os.makedirs(splits_dir, exist_ok=True)
    for ind in range(splits):
        image = Image.fromarray(shares[:,:,:,ind].astype(np.uint8))
        name = f"image_part_{ind+1}.png"
        part_paths.append(name)
        image.save(f"{splits_dir}\{name}")
        
    return part_paths

def rejoin(splits_dir, splits, img_output):
    shares = []
    
    for ind in range(splits):
        image_path = f"{splits_dir}/image_part_{ind+1}.png"
        image = Image.open(image_path)
        shares.append(np.asarray(image))
    
    shares = np.stack(shares, axis=-1)

    shares_image = shares.copy()
    for i in range(splits-1):
        shares_image[:,:,:,-1] = shares_image[:,:,:,-1] ^ shares_image[:,:,:,i]

    final_output = shares_image[:,:,:,splits-1]
    output_image = Image.fromarray(final_output.astype(np.uint8))
    output_image.save(f"media/{img_output}")
    
    return img_output