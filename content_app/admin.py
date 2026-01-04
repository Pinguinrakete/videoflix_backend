from django.contrib import admin
from django import forms
from .models import Video


class VideoAdminForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Feld thumbnail_url sichtbar, aber deaktiviert
        self.fields['thumbnail_url'].disabled = True


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    form = VideoAdminForm
    list_display = ("title", "category", "created_at", "thumbnail_url")
