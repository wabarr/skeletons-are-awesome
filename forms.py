from ajax_select.fields import AutoCompleteSelectField
from skeletons.models import *

from django.forms import ModelForm

class SpecimenFormForAJAXselect(ModelForm):
    class Meta:
        model = Specimen
        fields=["dropbox_glb_file_path"]

    search_by_name = AutoCompleteSelectField("specimens", required=False, help_text=None)

