import os
import random

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