from django.shortcuts import render

def signin(request):
    return render(request, 'accounts/in.html')


def signup(request):
    return render(request, 'accounts/up.html')


def signout(request):
    pass