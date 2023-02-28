from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'users/index.html')

def create(request): 
    if request.method == 'POST':
        pass
    return render(request,'users/create.html')

def edit(request, user):
    user = {'name': 'Juan', 'last_name': 'Perez', 'email': 'mack@@@.com'}    
    if request.method == 'POST':
        pass
    
    return render(request,'users/update.html', {'user': user})

def delete(request):
    if request.method == 'POST':
        pass
    return render(request,'users/delete.html')



    
    

