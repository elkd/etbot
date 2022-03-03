from django import forms
from PIL import Image

from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from autopost.models import ScheduledPost


ALLOWED_UPLOAD_IMAGES = ('png', 'jpeg', 'jpg')


class UploadForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get("image")
        if image:
            # This won't raise an exception since it was validated by ImageField.
            im = Image.open(image)

            if im.format.lower() not in ALLOWED_UPLOAD_IMAGES:
                raise forms.ValidationError(
                        "Unsupported file format. Supported formats are %s."
                        % ", ".join(ALLOWED_UPLOAD_IMAGES)
                      )
            image.seek(0)

        content = cleaned_data.get("content")
        try:
            str(content).encode('ascii')
        except UnicodeEncodeError:
            raise forms.ValidationError(
                    'Please enter all your details in English and ASCII characters (No Emojis or special characters)'
                    )

    class Meta:
        model = ScheduledPost
        fields = ["user", "author", "content", "image","post_time"]
