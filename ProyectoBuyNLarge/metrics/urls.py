from django.urls import path

from .views import TablaView, GraphicsView, KPIView

urlpatterns = [
    path('v1/table_data/', TablaView.as_view(), name='table_data'),
    path('v1/graphics_data/', GraphicsView.as_view(), name='graphics_data'),
    path('v1/kpi_data/', KPIView.as_view(), name='kpi_data'),
]