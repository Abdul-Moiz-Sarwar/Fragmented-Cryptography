import os
import random
import random
import string
def generate_keys(seed):
    random.seed(seed)

    # Substitution key: map ASCII characters (32 to 126) to a shuffled version
    characters = [chr(i) for i in range(32, 127)]
    shuffled_characters = characters[:]
    random.shuffle(shuffled_characters)
    substitution_key = dict(zip(characters, shuffled_characters))
    reverse_substitution_key = {v: k for k, v in substitution_key.items()}

    # Permutation key: generate a shuffled list of indices for text rearrangement
    permutation_key = list(range(len(characters)))
    random.shuffle(permutation_key)
    reverse_permutation_key = [0] * len(permutation_key)
    for i, p in enumerate(permutation_key):
        reverse_permutation_key[p] = i

    return substitution_key, reverse_substitution_key, permutation_key, reverse_permutation_key


def encrypt(text_input, seed, text_output):
    with open(text_input, 'r', encoding='utf-8') as f:
        data = f.read()

    substitution_key, _, permutation_key, _ = generate_keys(seed)


    # Substitution step
    substituted = ''.join(substitution_key.get(char, char) for char in data)

    # Permutation step
    # Pad the text to ensure its length is a multiple of the permutation key length
    block_size = len(permutation_key)
    padding_length = (block_size - len(substituted) % block_size) % block_size
    substituted += ' ' * padding_length

    encrypted = []
    for i in range(0, len(substituted), block_size):
        block = substituted[i:i + block_size]
        permuted_block = ''.join(block[j] for j in permutation_key)
        encrypted.append(permuted_block)

    with open(f"media/{text_output}", 'w', encoding='utf-8') as f:
        f.write(''.join(encrypted))

def decrypt(text_input, seed, text_output):
    with open(text_input, 'r', encoding='utf-8') as ef:
        data = ef.read()

    _, reverse_substitution_key, _, reverse_permutation_key = generate_keys(seed)


    # Reverse permutation step
    block_size = len(reverse_permutation_key)
    decrypted = []
    for i in range(0, len(data), block_size):
        block = data[i:i + block_size]
        unpermuted_block = ''.join(block[reverse_permutation_key[j]] for j in range(len(block)))
        decrypted.append(unpermuted_block)

    decrypted_text = ''.join(decrypted).rstrip()  # Remove padding

    # Reverse substitution step
    original = ''.join(reverse_substitution_key.get(char, char) for char in decrypted_text)

    with open(f"media/{text_output}", 'w', encoding='utf-8') as f:
        f.write(original)


def split_ascii_value(ascii_value, splits):
    buckets = [ascii_value // splits] * splits
    remaining = ascii_value % splits

    for i in range(remaining):
        buckets[i] += 1
    
    for i in range(splits):
        if buckets[i] > 3:
            value_to_move = random.randint(1, buckets[i] // 2)
            target_bucket = random.choice([j for j in range(splits) if j != i])
            buckets[i] -= value_to_move
            buckets[target_bucket] += value_to_move
    
    return buckets

def split(text_input, splits, splits_dir):
    os.makedirs(splits_dir, exist_ok=True)

    with open(text_input, 'r', encoding='utf-8', newline='') as file:
        content = file.read()

    split_files = []
    part_paths = []
    for split in range(splits):
        name = f'text_part_{split + 1}.txt'
        split_filename = os.path.join(splits_dir, name)
        split_files.append(open(split_filename, 'w', encoding='utf-8',  newline=''))
        part_paths.append(name)

    for char in content:
        ascii_value = ord(char)

        buckets = split_ascii_value(ascii_value, splits)

        for split, value in enumerate(buckets):
            split_files[split].write(chr(value))

    for split_file in split_files:
        split_file.close()

    return part_paths

def rejoin(splits_dir, splits, text_output):

    parts = []
    for i in range(splits):
        split_filename = os.path.join(splits_dir, f'text_part_{i + 1}.txt')
        with open(split_filename, 'r', encoding='utf-8', newline='') as split_file:
            parts.append(split_file.read())
    
    original_content = ""
    for i in range(len(parts[0])):
        ascii_value = 0
        for j in range(splits):
            value = ord(parts[j][i])
            ascii_value += value
        original_content += chr(ascii_value)

    with open(f"media/{text_output}", 'w', encoding='utf-8', newline='') as output_file:
        output_file.write(original_content)
    
    return text_output