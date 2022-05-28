from django.shortcuts import render, redirect
from .models import Image
from .form import ImageForm
from .ml import HAM10000


# Create your views here.
def homeview(request):
    msg = 'Upload as many files as you want!'

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            new_image = Image(image_file=request.FILES['image_file'])
            new_image.save()

            return redirect('home')
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        # empty form
        form = ImageForm()

    # load images for the list page
    images = Image.objects.all()

    context = {
        'msg': msg,
        'images': images,
        'form': form
    }

    return render(request, "backend/home.html", context)


def imageview(request, pk):
    image = Image.objects.get(id=pk)

    path = image.image_file.url
    print(path)
    pred = HAM10000(path)

    context = {
        'image': image,
        'pred': pred,
    }
    return render(request, 'backend/image.html', context)
