import numpy as np
from PIL import Image
import os

def logistic_map(size, seed):
    chaotic_seq = np.zeros(size, dtype=np.float64)
    x = seed
    r = 4
    for i in range(size):
        x = r * x * (1 - x)
        chaotic_seq[i] = x
    return (chaotic_seq * 255).astype(np.uint8) 

def encrypt(image_input, seed, image_output):
    input_image = Image.open(image_input)
    img_array = np.asarray(input_image)
    
    chaotic_key = logistic_map(img_array.size, seed)
    chaotic_key = chaotic_key.reshape(img_array.shape) 

    encrypted_img_array = np.bitwise_xor(img_array, chaotic_key)
    permutation_seq = logistic_map(img_array.size, seed + 0.1).argsort()
    encrypted_img_array = encrypted_img_array.flatten()[permutation_seq] 
    encrypted_img_array = encrypted_img_array.reshape(img_array.shape)
    
    encrypted_image = Image.fromarray(encrypted_img_array.astype(np.uint8))
    encrypted_image.save(f"media/{image_output}")

def decrypt(image_input, seed, image_output):
    input_image = Image.open(image_input)
    encrypted_img_array = np.asarray(input_image)
    
    encrypted_img_flat = encrypted_img_array.flatten()
    
    permutation_seq = logistic_map(encrypted_img_array.size, seed + 0.1).argsort()
    reverse_permutation = np.argsort(permutation_seq)
    
    unpermuted_img_flat = encrypted_img_flat[reverse_permutation]
    unpermuted_img_array = unpermuted_img_flat.reshape(encrypted_img_array.shape)

    
    chaotic_key = logistic_map(unpermuted_img_array.size, seed)
    chaotic_key = chaotic_key.reshape(unpermuted_img_array.shape)

    decrypted_img_array = np.bitwise_xor(unpermuted_img_array, chaotic_key)

    decrypted_image = Image.fromarray(decrypted_img_array.astype(np.uint8))
    decrypted_image.save(f"media/{image_output}")

def split(image_input, splits, splits_dir):
    input_image = Image.open(image_input)
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

def rejoin(splits_dir, splits, image_output):
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
    output_image.save(f"media/{image_output}")