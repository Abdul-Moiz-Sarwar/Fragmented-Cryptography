from .settings import MEDIA_ROOT, MEDIA_BASE_URL
from django.shortcuts import render
from . import audio, image, text

def upload_file(request):
    if request.method == 'POST':
        file_type = request.POST.get('file_type')
        plain_file = request.FILES.get('plain_file')
        splits = int(request.POST.get('segments', 2))
        encrypt = 'encrypt' in request.POST

        if file_type == 'image':
            response = {}

            file_state = f"original_{plain_file.name}"

            original_image_path = f"{MEDIA_ROOT}\{file_state}"
            response[f"original_image"] = f"{MEDIA_BASE_URL}{file_state}"

            with open(original_image_path, 'wb') as f:
                f.write(plain_file.read())

            if encrypt:
                file_state = f"encrypted_{plain_file.name}"

                image_path = f"{MEDIA_ROOT}\{file_state}"
                response["encrypted_image"] = f"{MEDIA_BASE_URL}{file_state}"

                image.encrypt(original_image_path, 0.5, file_state)
            else:
                image_path = original_image_path

            segments = image.split(image_path, splits, f"{MEDIA_ROOT}\image_splits")
            response["segments"] = [f"{MEDIA_BASE_URL}image_splits\{segment}" for segment in segments]

            file_state = f"reconstructed_{plain_file.name}"

            reconstructed_image_path = f"{MEDIA_ROOT}\{file_state}"
            response["reconstructed_image"] = f"{MEDIA_BASE_URL}{file_state}"

            image.rejoin(f"{MEDIA_ROOT}\image_splits", len(segments), file_state)

            if encrypt:
                file_state = f"decrypted_{plain_file.name}"
                response["decrypted_image"] = f"{MEDIA_BASE_URL}{file_state}"     
                image.decrypt(reconstructed_image_path, 0.5, file_state)

            return render(request, 'image.html', response)
        
        elif file_type == 'audio':
            response = {}

            file_state = f"original_{plain_file.name}"

            original_audio_path = f"{MEDIA_ROOT}\{file_state}"
            response["original_audio"] = f"{MEDIA_BASE_URL}{file_state}"

            with open(original_audio_path, 'wb') as f:
                f.write(plain_file.read())

            if encrypt:
                file_state = f"encrypted_{plain_file.name}"

                audio_path = f"{MEDIA_ROOT}\{file_state}"
                response["encrypted_audio"] = f"{MEDIA_BASE_URL}{file_state}"

                audio.encrypt(original_audio_path, 0.5, file_state)
            else:
                audio_path = original_audio_path

            segments = audio.split(audio_path, splits, f"{MEDIA_ROOT}\\audio_splits")
            response["segments"] = [f"{MEDIA_BASE_URL}audio_splits\{segment}" for segment in segments]

            file_state = f"reconstructed_{plain_file.name}"

            response["reconstructed_audio"] = f"{MEDIA_BASE_URL}{file_state}"
            reconstructed_audio_path = f"{MEDIA_ROOT}\{file_state}"

            audio.rejoin(f"{MEDIA_ROOT}\\audio_splits", len(segments), file_state)
            
            if encrypt:
                file_state = f"decrypted_{plain_file.name}"
                response["decrypted_audio"] = f"{MEDIA_BASE_URL}{file_state}"
                audio.decrypt(reconstructed_audio_path, 0.5, file_state)

                decrypted_audio_path = f"{MEDIA_ROOT}\{file_state}"
                with open(decrypted_audio_path, 'wb') as f:
                    plain_file.seek(0)
                    f.write(plain_file.read())

            return render(request, 'audio.html', response)
        
        elif file_type == 'text':
            response = {}

            file_state = f"original_{plain_file.name}"

            original_text_path = f"{MEDIA_ROOT}\{file_state}"
            response["original_text"] = f"{MEDIA_BASE_URL}{file_state}"

            with open(original_text_path, 'wb') as f:
                f.write(plain_file.read())
            
            if encrypt:
                file_state = f"encrypted_{plain_file.name}"

                text_path = f"{MEDIA_ROOT}\{file_state}"
                response["encrypted_text"] = f"{MEDIA_BASE_URL}{file_state}"

                text.encrypt(original_text_path, 0.5, file_state)
            else:
                text_path = original_text_path

            segments = text.split(text_path, splits, f"{MEDIA_ROOT}\\text_splits")
            response["segments"] = [f"{MEDIA_BASE_URL}text_splits\{segment}" for segment in segments]
            
            file_state = f"reconstructed_{plain_file.name}"

            reconstructed_text_path = f"{MEDIA_ROOT}\{file_state}"
            response["reconstructed_text"] = f"{MEDIA_BASE_URL}{file_state}"

            text.rejoin(f"{MEDIA_ROOT}\\text_splits", len(segments), f"reconstructed_{plain_file.name}")

            if encrypt:
                file_state = f"decrypted_{plain_file.name}"
                response["decrypted_text"] = f"{MEDIA_BASE_URL}{file_state}"
                text.decrypt(reconstructed_text_path, 0.5, file_state)

            return render(request, 'text.html', response)

    return render(request, 'form.html')