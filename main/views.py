from django.shortcuts import render

def show_main(request):
    context = {
        'npm' : '2306220753',
        'name': 'Daniel Liman',
        'class': 'PBP F'
    }

    return render(request, "main.html", context)
