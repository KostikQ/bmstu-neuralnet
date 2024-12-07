import io
from venv import logger

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from sympy import false

from excavators_detector.forms import ImageForm
from excavators_detector.process_image import process
from neuralnet import settings


# Create your views here.
def index(request):
    path_to_page = render_to_string('excavators_detector/excdet.html')
    return HttpResponse(path_to_page)

def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        uploaded_image = request.FILES['image']
        image_data = uploaded_image.read()
        #image = process(image_data)
        #form = ImageForm(request.POST, request.FILES)
        try:
            processed_image_array = process(image_data)
        except (IOError, SyntaxError):
            return render(request, 'excdet.html', {
                'form': ImageForm(),
                'error': 'Файл поврежден или не является изображением.'
            })
        # Преобразование numpy массива обратно в Pillow Image
        processed_image = Image.fromarray(processed_image_array)

        # Преобразование изображения в байтовый поток
        image_io = io.BytesIO()
        processed_image.save(image_io, format='JPEG')  # Например, сохраняем как JPEG

        # Создание нового InMemoryUploadedFile для формы
        image_io.seek(0)  # Возврат в начало потока
        new_image = InMemoryUploadedFile(
            image_io,  # Файл как байтовый поток
            'image',  # Поле, связанное с файлом
            uploaded_image.name,  # Оригинальное имя файла
            'image/jpeg',  # MIME тип
            image_io.getbuffer().nbytes,  # Размер файла
            None  # Дополнительные параметры, например, charset
        )

        # Замена загруженного изображения в форме
        form = ImageForm(request.POST, {'image': new_image})
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
            print(f"MEDIA_URL: {settings.MEDIA_URL}")
            print(f"Image URL: {img_obj.image.url}")
            import os
            print(os.access("C:\\Univer\\Usability\\Labs\\bmstu-neuralnet\\media\\images\\sany-sy335c_DYbzaqL.jpg",
                            os.R_OK))
            return render(request, 'excdet.html', {'form': form, 'img_obj': img_obj, 'error': False})
            # return render(request, 'excdet.html', {'form': form, 'image_url': 'images/sany-sy335c_VjEATAo.jpg', 'error': False})
    else:
        form = ImageForm()
    return render(request, 'excdet.html', {'form': form})