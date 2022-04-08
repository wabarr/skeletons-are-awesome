from django.core.management.base import BaseCommand
import csv
from skeletons.models import Element, Reference, Taxon

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open("./skeletons/fixtures/elements.csv", mode="r", encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                #print(row)
                numerical_identifier = row['numerical_identifier']
                if not numerical_identifier:
                    numerical_identifier = None
                Element.objects.get_or_create(name=row['name'],
                                              region=row['region'],
                                              subregion=row['subregion'],
                                              axial_appendicular=row['axial_appendicular'],
                                              positional_identifier=row['positional_identifier'],
                                              numerical_identifier=numerical_identifier
                                              )

        with open("./skeletons/fixtures/refsdump.csv", mode="r", encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row['volume']:
                    vol=None
                if not row['issue']:
                    issue=None


                Reference.objects.get_or_create(
                    authorshortstring=row['authorshortstring'],
                    year=row['year'],
                    journal=row['journal'],
                    volume=vol,
                    issue=issue,
                    pages=row['pages'],
                    doi=row['doi'],
                    dataEntryComplete=row['dataEntryComplete']
                                              )

        with open("./skeletons/fixtures/taxonomydump.csv", mode="r", encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    Taxon.objects.get_or_create(
                        kingdom=row['kingdom'],
                        phylum=row['phylum'],
                        tclass=row['tclass'],
                        order=row['order'],
                        family=row['family'],
                        subfamily=row['subfamily'],
                        tribe=row['tribe'],
                        genus=row['genus'],
                        species=row['species'],
                        infraspecificEpithet=row['infraspecificEpithet'],
                        identificationQualifier=row['identificationQualifier'],
                        extant=row['extant'],
                        commonName=row['commonName'],
                        #synonyms=row['synonyms'],
                        taxonRank=row['taxonRank'],
                        ref=Reference.objects.get(pk=row['ref_id'])
                    )
                except:
                    pass



