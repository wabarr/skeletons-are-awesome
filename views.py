from django.shortcuts import  render
from django.views.generic import ListView, DetailView
from .models import Skeleton, Specimen
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required(login_url="/admin/login/")
def home(request):
    return render(request, 'skeletons/home.html', {})

def grid(request):
    context = {}
    context['glbs'] = Specimen.objects.exclude(dropbox_glb_file_path__exact="").order_by("skeleton__taxon")
    return render(request,
                  'skeletons/grid.html',
                  context=context
    )

class SkeletonListView(LoginRequiredMixin,ListView):
    model = Skeleton
    paginate_by = 25
    login_url = "/admin/login/"

    def get_queryset(self):
        filters = {}
        tclass = self.request.GET.get('tclass')
        if tclass:
            filters['taxon__tclass']=tclass
        order = self.request.GET.get('order')
        if order:
            filters['taxon__order']=order
        family = self.request.GET.get('family')
        if family:
            filters['taxon__family']=family
        tribe =  self.request.GET.get('tribe')
        if tribe:
            filters['taxon__tribe']=tribe
        genus = self.request.GET.get('genus')
        if genus:
            filters['taxon__genus']=genus
        if not filters:
            new_queryset = Skeleton.objects.all()
        else:
            new_queryset = Skeleton.objects.filter(**filters)
        return(new_queryset)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SkeletonListView, self).get_context_data(**kwargs)
        context["orders"]= Skeleton.objects.values('taxon__order').distinct()
        context["family"] = Skeleton.objects.values('taxon__family').distinct()
        context["tribe"] = Skeleton.objects.values('taxon__tribe').distinct()
        context["genus"] = Skeleton.objects.values('taxon__genus').distinct()
        return(context)

class SpecimenDetailView(LoginRequiredMixin,DetailView):
    model = Specimen
    login_url = "/admin/login/"
