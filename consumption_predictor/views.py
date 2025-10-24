from django.shortcuts import render

def homepage(request):
    return render(request, 'consumption_predictor/homepage.html')