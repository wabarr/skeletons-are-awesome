from django.shortcuts import  render
from django.views.generic import ListView, DetailView
from .models import Skeleton, Specimen
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import logout
from django.views.generic.edit import FormView
from skeletons.forms import SpecimenFormForAJAXselect, MultipleSpecimenFormForAJAXselect
from django.http import JsonResponse
from skeletons.models import Specimen


def getGLBurl(request, pk):
    # this is a simple JSON url which returns the GLB file url for a given pk
    # it is used by the search.html template to convert the pk from the ajax_select query
    #into the GLB file path needed to populate the 3D model viewer
    ob = Specimen.objects.get(pk=pk)
    if ob.DO_spaces_glb_file_path:
        url = ob.DO_spaces_glb_file_path
    elif ob.dropbox_glb_file_path:
        url = "https://dl.dropboxusercontent.com/s/" + ob.dropbox_glb_file_path
    else:
        return JsonResponse({"error":"Can't find the link to the scan file"})

    if ob.side:
        elem = ob.side + " " + ob.element.__str__()
    else:
        elem = ob.element.__str__()

    return JsonResponse({"url": url,
                             "element": elem,
                             "taxon": ob.skeleton.taxon.__str__(),
                             "repo": ob.skeleton.repository.__str__(),
                             "specID": ob.skeleton.specimen_number})

#class Compare(LoginRequiredMixin,FormView):
class Compare(FormView):
    template_name = "skeletons/compare.html"
    form_class = MultipleSpecimenFormForAJAXselect
#class Grid(LoginRequiredMixin, ListView):
class Grid(ListView):
    template_name = 'skeletons/grid.html'
    queryset = Specimen.objects.exclude(dropbox_glb_file_path__exact="").order_by("skeleton__taxon")
    paginate_by = 18

class Search(FormView):
#class Search(LoginRequiredMixin, FormView):
    template_name = 'skeletons/search.html'
    form_class = SpecimenFormForAJAXselect

class SkeletonListView(ListView):
#class SkeletonListView(LoginRequiredMixin,ListView):
    model = Skeleton
    paginate_by = 25

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

class SpecimenDetailView(DetailView):

#class SpecimenDetailView(LoginRequiredMixin,DetailView):
    model = Specimen

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
