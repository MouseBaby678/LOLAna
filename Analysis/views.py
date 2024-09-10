from django.shortcuts import render

# Create your views here.
def index(request):

    roles = ["weqw","dasd"]
    return render(request,'index.html')
def aram(request):
    return render(request, 'aram.html')

def arena(request):
    return render(request, 'arena.html')

def bestteam_aram(request):
    return render(request, 'bestteam_aram.html')

def bestteam_arena(request):
    return render(request, 'bestteam_arena.html')

def bestteam_normal(request):
    return render(request, 'bestteam_normal.html')

def bottom(request):
    return render(request, 'bottom.html')

def jungle(request):
    return render(request, 'jungle.html')

def middle(request):
    return render(request, 'middle.html')

def ranked_flex(request):
    return render(request, 'ranked_flex.html')

def ranked_solo(request):
    return render(request, 'ranked_solo.html')

def support(request):
    return render(request, 'support.html')

def top(request):
    return render(request, 'top.html')
