from django.db import models
from django.utils.translation import ugettext_lazy as _


class Palette(models.Model):
    image = models.ImageField(verbose_name=_("Image"), upload_to='images/')
    colors = models.TextField(verbose_name=_("Colors"))
    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("Palette")
        verbose_name_plural = _("Palettes")
        ordering = ('-created_at',)

    def __str__(self):
        return self.image.path
