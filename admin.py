from django.contrib import admin
from .models import *
from ajax_select import make_ajax_form



class SkeletonAdmin(admin.ModelAdmin):
    fields = ['repository', 'collection_code', 'specimen_number', 'taxon','sex']
    form = make_ajax_form(Skeleton,{'taxon':"taxa"})


class ScannerAdmin(admin.ModelAdmin):
    fields = ['manufacturer','model','nickname']

class RepositoryAdmin(admin.ModelAdmin):
    fields = ['code','full_name', 'notes']

class SpecimenAdmin(admin.ModelAdmin):
    fields = ['filename','skeleton','element','side','specimen_label','dropbox_glb_file_path','dropbox_ply_file_path','scanned_by','date_scanned','machine']
    list_display = fields
    readonly_fields = ['filename']
    form = make_ajax_form(Specimen, {'element': "elements"})

class ElementAdmin(admin.ModelAdmin):
    fields = ['name', 'region', 'subregion', 'axial_appendicular','positional_identifier','numerical_identifier']
    list_display = ['__str__', 'region', 'subregion', 'axial_appendicular']
    list_display_links = ["__str__"]
    search_fields = ["name", "positional_identifier", "numerical_identifier"]

class TaxonAdmin(admin.ModelAdmin):
    list_display = ['__str__','order','family','tribe','genus','species','ref','extant']
    list_filter = ['taxonRank','tribe', "family"]
    search_fields = ["id","genus", "species", "tribe", "subfamily", "family", "order"]
    list_editable = ['extant','ref']

    @admin.display(description='Name')
    def __str__(self, obj):
        return obj.__unicode__()

class ReferenceAdmin(admin.ModelAdmin):
    list_display = ["authorshortstring", "year"]
    list_editable = ["year"]

admin.site.register(Skeleton, SkeletonAdmin)
admin.site.register(Scanner, ScannerAdmin)
admin.site.register(Specimen, SpecimenAdmin)
admin.site.register(Repository, RepositoryAdmin)
admin.site.register(Element, ElementAdmin)
admin.site.register(Reference, ReferenceAdmin)
admin.site.register(Taxon,TaxonAdmin)

admin.site.site_header = 'Skeletons are Awesome Admin Site'