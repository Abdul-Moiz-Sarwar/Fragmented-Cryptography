import numpy as np
import os, io, wave
from pydub import AudioSegment

def logistic_map(size, seed):
    chaotic_seq = np.zeros(size, dtype=np.float64)
    x = seed
    r = 4
    for i in range(size):
        x = r * x * (1 - x)
        chaotic_seq[i] = x
    chaotic_seq = chaotic_seq - np.floor(chaotic_seq)
    return ((chaotic_seq * 65535 - 32768)).astype(np.int16)

def encrypt(audio_input, seed, audio_output):
    audio = AudioSegment.from_file(audio_input)
    samples = np.array(audio.get_array_of_samples(), dtype=np.int16)

    chaotic_key = logistic_map(samples.size, seed)
    encrypted_samples = np.bitwise_xor(samples, chaotic_key)

    permutation_seq = logistic_map(samples.size, seed + 0.1).argsort()
    encrypted_samples = encrypted_samples[permutation_seq]

    encrypted_audio = audio._spawn(encrypted_samples.tobytes())
    encrypted_audio.export(f"media/{audio_output}", format="mp3")

def decrypt(audio_input, seed, audio_output):
    audio = AudioSegment.from_file(audio_input)
    encrypted_samples = np.array(audio.get_array_of_samples(), dtype=np.int16)

    permutation_seq = logistic_map(encrypted_samples.size, seed + 0.1).argsort()
    reverse_permutation = np.argsort(permutation_seq)
    
    unpermuted_samples = encrypted_samples[reverse_permutation]
    chaotic_key = logistic_map(unpermuted_samples.size, seed)
    decrypted_samples = np.bitwise_xor(unpermuted_samples, chaotic_key)

    decrypted_audio = audio._spawn(decrypted_samples.tobytes())
    decrypted_audio.export(f"media/{audio_output}", format="mp3")

def split(audio_input, parts, splits_dir):
    wav = AudioSegment.from_mp3(audio_input)

    wav_io = io.BytesIO()
    wav.export(wav_io, format="wav")
    wav_io.seek(0)

    with wave.open(wav_io, 'rb') as wav:
        params = wav.getparams()
        n_channels, sampwidth, framerate, n_frames, comptype, compname = params
        frames = wav.readframes(n_frames)

    audio = np.frombuffer(frames, dtype=np.int16)
    audio_length = len(audio)

    np.random.seed(42)
    masks = [np.random.randint(-2**15, 2**15, audio_length, dtype=np.int16) for _ in range(parts - 1)]
    masked_sum = sum(masks)
    last_part = audio - masked_sum

    os.makedirs(splits_dir, exist_ok=True)
    all_parts = masks + [last_part]
    part_paths = []
    for idx, part in enumerate(all_parts):
        name = f"audio_part_{idx+1}.wav"
        part_wav_path = os.path.join(splits_dir, name)
        with wave.open(part_wav_path, 'wb') as part_file:
            part_file.setparams((n_channels, sampwidth, framerate, len(part), comptype, compname))
            part_file.writeframes(part.tobytes())
        part_paths.append(name)

    return part_paths

def rejoin(splits_dir, parts, audio_output):
    audio_parts = []
    for idx in range(parts):
        with wave.open(os.path.join(splits_dir, f"audio_part_{idx+1}.wav"), 'rb') as part_file:
            frames = part_file.readframes(part_file.getnframes())
            audio_parts.append(np.frombuffer(frames, dtype=np.int16))

    reconstructed = sum(audio_parts)

    with wave.open(f"media/{audio_output}", 'wb') as output_file:
        params = part_file.getparams()
        output_file.setparams(params)
        output_file.writeframes(reconstructed.tobytes())

    return audio_output