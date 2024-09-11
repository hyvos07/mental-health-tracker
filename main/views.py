from django.shortcuts import render, redirect   # Tambahkan import redirect di baris ini
from main.forms import MoodEntryForm
from main.models import MoodEntry
from django.http import HttpResponse, JsonResponse
from django.core import serializers


# Show Main Page with lists of Mood Entries
def show_main(request):
    mood_entries = MoodEntry.objects.all()

    context = {
        'name': 'Pak Bepe',
        'class': 'PBP D',
        'npm': '2306123456',
        'mood_entries': mood_entries
    }

    return render(request, "main.html", context)


# Create new data of Moods
def create_mood_entry(request):
    form = MoodEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_mood_entry.html", context)


# Show XML of all data
def show_xml(request):
    data = MoodEntry.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")


# Show JSON of all data
def show_json(request):
    data = MoodEntry.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


# Show XML by ID
def show_xml_by_id(request, id):
    data = MoodEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")


# Show JSON by ID
def show_json_by_id(request, id):
    data = MoodEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
