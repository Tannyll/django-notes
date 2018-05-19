from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, FormView, DeleteView
from hello_palette.models import Palette
from hello_palette.forms import PaletteForm


class PaletteFormView(FormView):
    template_name = 'palette/new.html'
    form_class = PaletteForm

    def form_valid(self, form):
        palette = form.save()
        return redirect('palette:detail', palette.pk)


class PaletteDetailView(DetailView):
    template_name = 'palette/detail.html'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Palette, pk=pk, is_deleted=False)


class PaletteDeleteView(DeleteView):
    template_name = 'palette/delete.html'
    model = Palette

    def post(self, request, *args, **kwargs):
        palette = self.get_object()
        palette.is_deleted = True
        palette.save()
        return redirect('palette:new')
