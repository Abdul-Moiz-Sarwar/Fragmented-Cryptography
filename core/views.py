from django.shortcuts import render
import os
from . import audio
from . import image
from . import text
from .settings import MEDIA_ROOT, MEDIA_URL, BASE_URL

def encrypt_image(file):
    return file

def decrypt_image(file):
    return file

def encrypt_audio(file):
    return file

def decrypt_audio(file):
    return file

def encrypt_text(file):
    return file

def decrypt_text(file):
    return file

def upload_file(request):
    if request.method == 'POST':
        file_type = request.POST.get('file_type')
        plain_file = request.FILES.get('plain_file')
        splits = int(request.POST.get('segments', 2))
        encrypt = 'encrypt' in request.POST

        if file_type == 'image':
            response = {}
            original_image_path = os.path.join(MEDIA_ROOT, f'_original_{plain_file.name}')
            with open(original_image_path, 'wb') as f:
                f.write(plain_file.read())

            response["original_image"] = f"{BASE_URL}{MEDIA_URL}_original_{plain_file.name}"

            if encrypt:
                image_path = encrypt_image(original_image_path)
                response["encrypted_image"] = f"{BASE_URL}{MEDIA_URL}_original_{plain_file.name}"
            else:
                image_path = original_image_path

            segments = image.split(image_path, splits, f"{MEDIA_ROOT}\image_splits")
            response["segments"] = [f"{BASE_URL}{MEDIA_URL}image_splits\{segment}" for segment in segments]
            print(response["segments"])


            reconstructed_image = image.rejoin(f"{MEDIA_ROOT}\image_splits", len(segments), f"_reconstructed_{plain_file.name}")
            response["reconstructed_image"] = f"{BASE_URL}{MEDIA_URL}{reconstructed_image}"
            print(response["reconstructed_image"])

            if encrypt:
                final_image_path = decrypt_image(reconstructed_image)
                response["decrypted_image"] = f"{BASE_URL}{MEDIA_URL}{final_image_path}"          

            return render(request, 'image.html', response)
        

        elif file_type == 'audio':
            response = {}
            original_audio_path = os.path.join(MEDIA_ROOT, f"_original_{plain_file.name}")
            with open(original_audio_path, 'wb') as f:
                f.write(plain_file.read())
                
            response["original_audio"] = f"{BASE_URL}{MEDIA_URL}_original_{plain_file.name}"
            print(response["original_audio"])

            if encrypt:
                audio_path = encrypt_audio(original_audio_path)
                response["encrypted_audio"] = f"{BASE_URL}{MEDIA_URL}_original_{plain_file.name}"
            else:
                audio_path = original_audio_path

            segments = audio.split(audio_path, splits, f"{MEDIA_ROOT}\\audio_splits")
            response["segments"] = [f"{BASE_URL}{MEDIA_URL}audio_splits\{segment}" for segment in segments]
            print(response["segments"])

            reconstructed_audio = audio.rejoin(f"{MEDIA_ROOT}\\audio_splits", len(segments), f"_reconstructed_{plain_file.name}")
            response["reconstructed_audio"] = f"{BASE_URL}{MEDIA_URL}{reconstructed_audio}"
            print(response["reconstructed_audio"])

            if encrypt:
                final_audio_path = decrypt_audio(reconstructed_audio)
                response["decrypted_audio"] = f"{BASE_URL}{MEDIA_URL}{final_audio_path}"

            return render(request, 'audio.html', response)
        

        elif file_type == 'text':
            response = {}
            original_text_path = os.path.join(MEDIA_ROOT, f'_original_{plain_file.name}')
            with open(original_text_path, 'wb') as f:
                f.write(plain_file.read())
            
            response["original_text"] = f"{BASE_URL}{MEDIA_URL}_original_{plain_file.name}"
            print(response["original_text"])

            if encrypt:
                text_path = encrypt_text(original_text_path)
                response["encrypted_text"] = f"{BASE_URL}{MEDIA_URL}_original_{plain_file.name}"
            else:
                text_path = original_text_path

            segments = text.split(text_path, splits, f"{MEDIA_ROOT}\\text_splits")
            response["segments"] = [f"{BASE_URL}{MEDIA_URL}text_splits/{segment}" for segment in segments]
            print(response["segments"])

            reconstructed_text = text.rejoin(f"{MEDIA_ROOT}\\text_splits", len(segments), f"_reconstructed_{plain_file.name}")
            response["reconstructed_text"] = f"{BASE_URL}{MEDIA_URL}{reconstructed_text}"
            print(response["reconstructed_text"])

            if encrypt:
                final_text_path = decrypt_text(reconstructed_text)
                response["decrypted_text"] = f"{BASE_URL}{MEDIA_URL}{final_text_path}"

            return render(request, 'text.html', response)


    return render(request, 'form.html')