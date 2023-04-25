from django.contrib import admin
from .models import *
from ajax_select import make_ajax_form



class SkeletonAdmin(admin.ModelAdmin):
    fields = ['repository', 'collection_code', 'specimen_number', 'taxon','sex','notes']
    list_display = ['__str__','taxon','sex','notes']
    search_fields = ["specimen_number","taxon__genus", "taxon__species", "taxon__order", "taxon__family", "taxon__subfamily", "taxon__tribe"]
    form = make_ajax_form(Skeleton,{'taxon':"taxa"})
    search_help_text = "Search by specimen number or taxon"
    list_filter = ["repository"]

class ScannerAdmin(admin.ModelAdmin):
    fields = ['manufacturer','model','nickname']

class RepositoryAdmin(admin.ModelAdmin):
    fields = ['code','full_name', 'notes']

class SpecimenAdmin(admin.ModelAdmin):
    fields = ['filename','skeleton','element','side','specimen_label','dropbox_glb_file_path','dropbox_ply_file_path','DO_spaces_glb_file_path','scanned_by','date_scanned','machine']
    list_display = fields
    readonly_fields = ['filename']
    form = make_ajax_form(Specimen, {'element': "elements", 'skeleton': 'skeletons'})
    list_filter = ["side","skeleton__repository"]
    search_fields = ["skeleton__specimen_number","element__name","skeleton__taxon__genus", "skeleton__taxon__species", "skeleton__taxon__order", "skeleton__taxon__family", "skeleton__taxon__subfamily", "skeleton__taxon__tribe"]
    search_help_text = "Search by specimen number, element, or taxon"

class ElementAdmin(admin.ModelAdmin):
    fields = ['name', 'region', 'subregion', 'axial_appendicular','positional_identifier','numerical_identifier']
    list_display = ['__str__', 'region', 'subregion', 'axial_appendicular']
    list_display_links = ["__str__"]
    search_fields = ["name", "positional_identifier", "numerical_identifier"]
    list_filter = ["region", "subregion", "axial_appendicular"]

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