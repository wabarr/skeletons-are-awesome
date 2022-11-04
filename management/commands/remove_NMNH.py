from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        from skeletons.models import Skeleton, Repository, Specimen

        usnm = Repository.objects.get(code="USNM")


        for skel in Skeleton.objects.filter(repository__code="NMNH"):
            skel.repository = usnm
            skel.save()

        for specimen in Specimen.objects.all():
            specimen.dropbox_glb_file_path = specimen.dropbox_glb_file_path.replace("NMNH", "USNM")
            specimen.dropbox_ply_file_path = specimen.dropbox_ply_file_path.replace("NMNH", "USNM")
            specimen.save()

        nmnh = Repository.objects.get(code="NMNH")
        nmnh.delete()
