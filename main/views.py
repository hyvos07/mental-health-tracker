import datetime
import json

from django.core import serializers
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags

from main.forms import MoodEntryForm
from main.models import MoodEntry
from main.utils.utils import time_ago


# Register Page
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form': form}
    return render(request, 'register.html', context)


# Logging In
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)


# Logging Out
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response


# Show Main Page with lists of Mood Entries
@login_required(login_url='/login')
def show_main(request):
    # mood_entries = MoodEntry.objects.filter(user=request.user)

    context = {
        'name': request.user.username,
        'class': 'PBP F',
        'npm': '2306220753',
        # 'mood_entries': mood_entries,
        'last_login': time_ago(request.COOKIES['last_login']),
    }

    return render(request, "main.html", context)


# Create new data of Moods
def create_mood_entry(request):
    form = MoodEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        mood_entry = form.save(commit=False)
        mood_entry.user = request.user
        mood_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_mood_entry.html", context)


# Add mood entry using AJAX
@csrf_exempt
@require_POST
def add_mood_entry_ajax(request):
    mood = strip_tags(request.POST.get("mood"))
    feelings = strip_tags(request.POST.get("feelings"))
    mood_intensity = request.POST.get("mood_intensity")
    user = request.user

    new_mood = MoodEntry(
        mood=mood, feelings=feelings,
        mood_intensity=mood_intensity,
        user=user
    )
    new_mood.save()

    return HttpResponse(b"CREATED", status=201)


# Update data of Moods
def edit_mood(request, id):
    mood = MoodEntry.objects.get(pk=id)

    form = MoodEntryForm(request.POST or None, instance=mood)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "edit_mood.html", context)


# Delete data of Moods
def delete_mood(request, id):
    mood = MoodEntry.objects.get(pk=id)
    mood.delete()
    return HttpResponseRedirect(reverse('main:show_main'))


# Show XML of all data
def show_xml(request):
    data = MoodEntry.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")


# Show JSON of all data
def show_json(request):
    data = MoodEntry.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


# Show XML by ID
def show_xml_by_id(request, id):
    data = MoodEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")


# Show JSON by ID
def show_json_by_id(request, id):
    data = MoodEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


# Make Mood Mobile
@csrf_exempt
def create_mood_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        new_mood = MoodEntry.objects.create(
            user=request.user,
            mood=data["mood"],
            mood_intensity=int(data["mood_intensity"]),
            feelings=data["feelings"]
        )

        new_mood.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
