from django.shortcuts import render,redirect
from .models import Category, Photo
from django.db.models import Q

def gallery(request):
    if'q' in request.GET:
        q = request.GET['q']
        multiple_q = Q(name__icontains=q)
        categories = Category.objects.filter(multiple_q)
    else:
        categories = Category.objects.all()
        photos = Photo.objects.all()
    
    context = {
        'categories': categories,
        'photos': photos

    }
    return render(request, 'gallery.html',context)

def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'photo.html', {'photo': photo})

def addPhoto(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')
        # print('data', data)
        # print('image', image)
        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
            category = None
        photo = Photo.objects.create(
            category=category,
            description=data['description'],
            image=image,
        )   
        return redirect("gallery")
    return render(request, 'add.html', {'categories': categories})