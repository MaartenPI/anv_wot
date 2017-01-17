from django.shortcuts import render, get_object_or_404

def homepage(request):

    return render(request, 'base.html')
