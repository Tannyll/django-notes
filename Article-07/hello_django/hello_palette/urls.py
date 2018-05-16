from django.urls import path
from hello_palette.views import PaletteDetailView, PaletteFormView, PaletteDeleteView

app_name = 'palette'

urlpatterns = [
    path('', view=PaletteFormView.as_view(), name='new'),
    path('<int:pk>/', view=PaletteDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', view=PaletteDeleteView.as_view(), name='delete'),
]
