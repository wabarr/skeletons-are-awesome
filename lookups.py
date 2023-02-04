from ajax_select import register, LookupChannel
from .models import Taxon, Element, Specimen
from django.db.models import Q, Value
from django.db.models.functions import Concat

@register('taxa')
class TaxonLookup(LookupChannel):

    model = Taxon

    def get_query(self, q, request):
        query = Q(taxonRank__icontains=q) | Q(species__icontains=q) | Q(genus__icontains=q) | Q(tribe__icontains=q) | Q(
            subfamily__icontains=q) | Q(family__icontains=q) | Q(tclass__icontains=q)
        return Taxon.objects.filter(query).exclude(taxonRank__exact="subspecies")

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.__str__()

    def can_add(self, user, argmodel):
        return True


@register('elements')
class ElementLookup(LookupChannel):

    model = Element

    def get_query(self, q, request):
        queryset = Element.objects.annotate(search_name=Concat('positional_identifier', Value(' '), 'name'))
        return queryset.filter(search_name__icontains=q)

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.__str__()

    def can_add(self, user, argmodel):
        return True

@register('specimens')
class SpecimenLookup(LookupChannel):

    model = Specimen

    def get_query(self, q, request):
        query = Q(element__name__icontains=q) | \
                Q(skeleton__taxon__taxonRank__icontains=q) | \
                Q(skeleton__taxon__species__icontains=q) | \
                Q(skeleton__taxon__genus__icontains=q) | \
                Q(skeleton__taxon__tribe__icontains=q) | \
                Q(skeleton__taxon__subfamily__icontains=q) | \
                Q(skeleton__taxon__family__icontains=q) | \
                Q(skeleton__taxon__tclass__icontains=q) | \
                Q(skeleton__specimen_number__icontains=q) | \
                Q(skeleton__repository__code__icontains=q) | \
                Q(skeleton__collection_code__icontains=q)
        return Specimen.objects.filter(query).order_by("skeleton__taxon")

    def format_item_display(self, item):
        return u"<span class='tag'>%s | %s | %s</span>" % (item.skeleton.taxon, item.skeleton, item.__str__())

    def format_match(self, item):
        return u"<span class='tag'>%s | %s | %s</span>" % (item.skeleton.taxon, item.skeleton, item.__str__())
