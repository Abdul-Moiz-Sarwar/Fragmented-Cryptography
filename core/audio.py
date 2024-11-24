import wave
import numpy as np
import os, io
from pydub import AudioSegment

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