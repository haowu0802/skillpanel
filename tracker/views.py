from django.shortcuts import render, redirect
from tracker.models import Log, Tracker

# Create your views here.


def home_page(request):
    return render(request, 'home.html')


def view_tracker(request):
    logs = Log.objects.all()
    return render(request, 'tracker.html', {
        'logs': logs,
    })


def new_tracker(request):
    """create a new tracker and redirect to its url"""
    tracker = Tracker.objects.create()
    Log.objects.create(text=request.POST['log_text'],
                       tracker=tracker)
    return redirect('/trackers/the-only-tracker/')
