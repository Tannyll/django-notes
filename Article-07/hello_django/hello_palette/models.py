from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from hello_palette.color_parser import ColorParser


class Palette(models.Model):
    image = models.ImageField(verbose_name=_("Image"), upload_to='images/')
    colors = models.TextField(verbose_name=_("Colors"), editable=False)
    is_deleted = models.BooleanField(verbose_name=_("Is deleted?"), blank=True, default=False)
    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("Palette")
        verbose_name_plural = _("Palettes")
        ordering = ('-created_at',)

    def __str__(self):
        return self.image.name

    @property
    def colors_as_list(self):
        return self.colors.split(',')


@receiver(models.signals.post_save, sender=Palette)
def parse_colors(sender, instance, created, **kwargs):
    if not created:
        return  # don't do anything

    instance.colors = ColorParser(image_path=instance.image.path).parse_colors()
    instance.save()
