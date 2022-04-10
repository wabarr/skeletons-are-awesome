from django.shortcuts import  render
from django.views.generic import ListView, DetailView
from .models import Skeleton, Specimen

def home(request):
    return render(request, 'skeletons/home.html', {})

class SkeletonListView(ListView):
    model = Skeleton

class SpecimenDetailView(DetailView):
    model = Specimen
