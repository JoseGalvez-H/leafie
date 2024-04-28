from django.shortcuts import render

# TODO REMOVE TEMP DATABASE
plants = [
    {'name': 'Lolo', 'type': 'pothos', 'description': 'big green leaves'},
    {'name': 'Lola', 'type': 'orchid', 'description': 'small stems'},
    {'name': 'Milo', 'type': 'rose', 'description': 'so many thorns'},
]

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def plants_index(request):
    return render(request, 'plants/index.html', {
        'plants': plants
    })
