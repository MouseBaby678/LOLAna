from django.shortcuts import render

# Create your views here.
def index(request):

    roles = ["weqw","dasd"]
    return render(request,'index.html')