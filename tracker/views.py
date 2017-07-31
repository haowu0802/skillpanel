from django.shortcuts import render, redirect
from tracker.models import Log

# Create your views here.


def home_page(request):
    if request.method == 'POST':
        Log.objects.create(text=request.POST['log_text'])
        return redirect('/')  # "always redirect after a POST", they say

    logs = Log.objects.all()
    return render(request, 'home.html', {
        'logs': logs,
    })

