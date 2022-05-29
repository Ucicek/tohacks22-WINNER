from django.shortcuts import render, redirect

# Create your views here.
# Create your views here.
def homeview(request):

    context = {
        'msg': 'hello world',
    }
    return render(request, "backend/home.html", context)
