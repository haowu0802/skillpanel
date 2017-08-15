from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from tracker.models import Log, Tracker

# Create your views here.


def home_page(request):
    return render(request, 'home.html')


def view_tracker(request, tracker_id):
    """list Logs for a Tracker"""
    tracker = Tracker.objects.get(id=tracker_id)
    return render(request, 'tracker.html', {
        'tracker': tracker,
    })


def new_tracker(request):
    """create a new tracker and redirect to its url"""
    tracker = Tracker.objects.create()
    log = Log.objects.create(text=request.POST['log_text'],
                             tracker=tracker)
    try:
        log.full_clean()
        log.save()
    except ValidationError:
        tracker.delete()
        error = "You can't save an empty log."
        return render(request, 'home.html', {'error': error})
    return redirect(f'/trackers/{tracker.id}/')


def add_log(request, tracker_id):
    """add a new Log to an existing Tracker"""
    tracker = Tracker.objects.get(id=tracker_id)
    Log.objects.create(text=request.POST['log_text'],
                       tracker=tracker)
    return redirect(f'/trackers/{tracker.id}/')
