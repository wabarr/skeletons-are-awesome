from django.core.management.base import BaseCommand

import supersecrets


class Command(BaseCommand):
    def handle(self, *args, **options):
        from skeletons.models import Specimen
        import boto3
        import botocore
        import requests
        import os

        session = boto3.session.Session()
        client = session.client('s3',
                                endpoint_url='https://nyc3.digitaloceanspaces.com',
                                config=botocore.config.Config(s3={'addressing_style': 'virtual'}),
                                # Configures to use subdomain/virtual calling format.
                                region_name='nyc3',
                                aws_access_key_id=supersecrets.DO_SPACES_KEY,
                                aws_secret_access_key=supersecrets.DO_SPACES_SECRETKEY)

        spec = Specimen.objects.filter(DO_spaces_glb_file_path='').exclude(dropbox_glb_file_path='').first()
        url = 'https://dl.dropboxusercontent.com/s/' + spec.dropbox_glb_file_path
        r = requests.get(url, allow_redirects=True)
        tempfilepath='temp.glb'
        f = open(tempfilepath, 'wb')
        f.write(r.content)
        f.close()
        client.upload_file(tempfilepath, Bucket="skeletons-are-awesome", Key=spec.filename() + ".glb", ExtraArgs={'ACL':'public-read'})
        test = requests.head("https://nyc3.digitaloceanspaces.com/" + "skeletons-are-awesome/" + spec.filename() + ".glb")
        if test.status_code == 200:
            spec.DO_spaces_glb_file_path="https://skeletons-are-awesome.nyc3.cdn.digitaloceanspaces.com/" + spec.filename() + '.glb'
            spec.save()
        else:
            pass
        os.remove('temp.glb')


