"""gaspro_sme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.views.generic import TemplateView

# from rest_framework_swagger.views import get_swagger_view
# from rest_framework.schemas import get_schema_view
# from rest_framework.documentation import include_docs_urls

urlpatterns = [s
    path("admin/", admin.site.urls),
    path('api/v2/accounts/', include('accounts.urls')),
    path('api/v2/assets/', include('asset.urls')),
    path('api/v2/auxilliary/', include('auxilliary.urls')),
    path('api/v2/billings/', include('billing.urls')),
    path('api/v2/meter-readings/', include('meter_readings.urls')),
    path('api/v2/orders/', include('orders.urls')),
    path('api/v2/retailers/', include('retailers.urls')),

    # Default Auth
    path('api/v2/api-auth/', include('rest_framework.urls')),
    path('api/v2/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v2/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    #path('swagger-docs/', schema_view),
    #path('docs/', include_docs_urls(title='HFV2 APIs')),
    #path('schema/', schema_view),
]
