from django.db import models
from .choices_taxonomy import *
from django.utils.encoding import smart_text
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.exceptions import ValidationError

class Reference(models.Model):
    authorshortstring = models.CharField(max_length=100, help_text="Author name as it would appear in an in-text citation.")
    year = models.IntegerField()
    journal = models.CharField(max_length=100, blank=True)
    volume = models.IntegerField(blank=True, null=True)
    issue = models.IntegerField(blank=True, null=True)
    pages = models.CharField(max_length=20, blank=True)
    doi = models.CharField(max_length=100, blank=True)
    dataEntryComplete = models.BooleanField(null=True, blank=True, default=False)

    def __str__(self):
        name = self.authorshortstring + ", " + str(self.year)
        return name


class Repository(models.Model):
    code = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=100)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "repositories"

    def __str__(self):
        return self.code


class Element(models.Model):
    AXIAL_APPENDICULAR = models.TextChoices('axial_appendicular', 'axial appendicular')
    REGION = models.TextChoices('region', 'skull thorax forelimb hindlimb')
    POSTIONS = models.TextChoices('positional_identifer', 'proximal intermediate distal')
    SUBREGION_CHOICES = [("cranium", "Cranium"),("middle ear", "Middle ear"),("mandible", "Mandible"),("ribs", "Ribs"),("hyoid", "Hyoid"),("sternum", "Sternum"),("vertebral Column", "Vertebral Column"),("shoulder Girdle", "Shoulder Girdle"),("proximal Forelimb", "Proximal Forelimb"),("distal Forelimb", "Distal Forelimb"),("wrist", "Wrist"),("manus (hand)", "Manus (Hand)"),("pelvic girdle", "Pelvic Girdle"),("proximal hindlimb", "Proximal Hindlimb"),("distal hindlimb", "Distal Hindlimb"),("ankle", "Ankle"),("pes (foot)", "Pes (Foot)")]

    name = models.CharField(max_length=100)
    axial_appendicular = models.CharField(max_length=100, choices=AXIAL_APPENDICULAR.choices)
    region = models.CharField(max_length=100, choices=REGION.choices, blank=True)
    subregion = models.CharField(max_length=100, choices=SUBREGION_CHOICES, blank=True)
    numerical_identifier = models.PositiveIntegerField(blank=True, null=True)
    positional_identifier = models.CharField(max_length=100, choices=POSTIONS.choices, blank=True)

    def __str__(self):
        if self.name in ["metacarpal", "metatarsal", "phalanx"]:
            return "{} {} {} {}".format(self.positional_identifier, self.name, self.numerical_identifier, self.subregion).replace("None","")
        else:
            return self.name
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['positional_identifier', 'name', 'numerical_identifier','subregion'], name='unique element')
        ]


class Taxon(models.Model):
    kingdom = models.CharField(max_length=100, blank=True, choices=CHOICES_KINGDOM, default="Animalia")
    phylum = models.CharField(max_length=100,  blank=True, choices=CHOICES_PHYLUM, default="Chordata")
    tclass = models.CharField(max_length=100,  blank=True, choices=CHOICES_CLASS, verbose_name="class")
    order = models.CharField(max_length=100,  blank=True, choices=CHOICES_ORDER)
    family = models.CharField(max_length=100,  blank=True)
    subfamily = models.CharField(max_length=100,  blank=True)
    tribe = models.CharField(max_length=100,  blank=True, choices=CHOICES_TRIBE)
    genus = models.CharField(max_length=100,  blank=True, verbose_name="genus")
    species = models.CharField(max_length=100,  blank=True, verbose_name="species")
    infraspecificEpithet = models.CharField(max_length=100,  blank=True)
    identificationQualifier = models.CharField(max_length=100,  blank=True, help_text="e.g. aff. or cf.")
    extant = models.BooleanField(default=True)
    commonName = models.CharField(max_length=100,  blank=True)
    synonyms = models.CharField(max_length=2000,  blank=True)
    taxonRank = models.CharField(max_length=100,  blank=False, choices=CHOICES_RANK)
    ref = models.ForeignKey(Reference, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if str(self.taxonRank).lower() == 'tclass':
            name = self.tclass + " (class)"
        elif str(self.taxonRank).lower() == 'order':
            name = self.order + " (" + self.taxonRank + ")"
        elif str(self.taxonRank).lower() == 'family':
            name = self.family + " (" + self.taxonRank + ")"
        elif str(self.taxonRank).lower() == 'subfamily':
            name = self.subfamily + " (" + self.taxonRank + ")"
        elif str(self.taxonRank).lower() == 'tribe':
            name = self.tribe + " (" + self.taxonRank + ")"
        elif str(self.taxonRank).lower() == 'genus':
            name = self.genus + " (" + self.taxonRank + ")"
        # special case for things like Alcelaphini sp. large of Reed 2008
        elif str(self.taxonRank).lower() == 'species' and self.genus == "":
            name = smart_text(self.tribe) + " " + smart_text(self.species) + " (" + smart_text(self.taxonRank) + ")"
        elif str(self.taxonRank).lower() == 'species':
            name = self.genus + " " + self.species + " (" + self.taxonRank + ")"
        elif str(self.taxonRank).lower() == 'subspecies':
            name = self.genus + " " + self.species + " " + self.infraspecificEpithet + " (" + self.taxonRank + ")"
        else:
            name = " (" + self.taxonRank + ")"

        if self.identificationQualifier:
            name = self.identificationQualifier + " " + name

        if not self.extant:
            name = smart_text(name) + " **"

        return smart_text(name)

    def validate_implied_taxon(self, rankString, **kwargs):
        modelFieldNames = [key for key in kwargs.keys()]
        modelFieldName = modelFieldNames[0] #assumes there is only one keyword!

        if getattr(self, modelFieldName):
            try:
                Taxon.objects.get(taxonRank=rankString, **kwargs)
            except MultipleObjectsReturned:
                pass
                ## pass, because there may be good reasons for why there are multiple entries
                # raise ValidationError(
                #     "This taxon implies a single entry for '{0}' at rank of {1}, but there are multiple entries in the database".format(
                #         getattr(self, modelFieldName), rankString)
                # )
            except ObjectDoesNotExist:
                raise ValidationError(
                    "This taxon implies the existence of a taxon called '{0}' at the rank of {1}. You must add the implied taxon before you can add this one.".format(
                        getattr(self, modelFieldName), rankString)
                )

    def clean(self):
        if self.taxonRank == "species":
            self.validate_implied_taxon('order', order=self.order)
            self.validate_implied_taxon('family', family=self.family)
            self.validate_implied_taxon('subfamily', subfamily=self.subfamily)
            self.validate_implied_taxon('tribe', tribe=self.tribe)
            self.validate_implied_taxon('genus', genus=self.genus)
        if self.taxonRank == "genus":
            self.validate_implied_taxon('order', order=self.order)
            self.validate_implied_taxon('family', family=self.family)
            self.validate_implied_taxon('subfamily', subfamily=self.subfamily)
            self.validate_implied_taxon('tribe', tribe=self.tribe)
        if self.taxonRank == "tribe":
            self.validate_implied_taxon('order', order=self.order)
            self.validate_implied_taxon('family', family=self.family)
            self.validate_implied_taxon('subfamily', subfamily=self.subfamily)
        if self.taxonRank == "subfamily":
            self.validate_implied_taxon('order', order=self.order)
            self.validate_implied_taxon('family', family=self.family)
        if self.taxonRank == "family":
            self.validate_implied_taxon('order', order=self.order)

    def validate_unique(self, exclude=None):
        try:
            match = Taxon.objects.filter(
                kingdom=self.kingdom,
                phylum=self.phylum,
                tclass=self.tclass,
                order=self.order,
                family=self.family,
                tribe=self.tribe,
                genus=self.genus,
                species=self.species,
                infraspecificEpithet=self.infraspecificEpithet,
                identificationQualifier=self.identificationQualifier,
                taxonRank=self.taxonRank
            ).exclude(pk=self.pk)
            if len(match) > 0:
                raise ValidationError({NON_FIELD_ERRORS: 'Matching taxon already exists'})
        except ObjectDoesNotExist:
            super(Taxon, self).validate_unique()

    class Meta:
        verbose_name_plural="Taxa"
        constraints=[
            models.UniqueConstraint(fields=['tclass', 'order', 'family', 'subfamily', 'tribe', 'genus', 'species',
                           'infraspecificEpithet', 'taxonRank', 'identificationQualifier'], name="unique taxon")
            ]


class Skeleton(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    collection_code = models.CharField(max_length=100, blank=True)
    specimen_number = models.PositiveIntegerField()
    taxon = models.ForeignKey(Taxon, on_delete=models.CASCADE)

    def __str__(self):
        return "{}-{}-{}".format(self.repository,self.collection_code,self.specimen_number).replace("--","-")

class Specimen(models.Model):
    skeleton = models.ForeignKey(Skeleton, on_delete=models.CASCADE)