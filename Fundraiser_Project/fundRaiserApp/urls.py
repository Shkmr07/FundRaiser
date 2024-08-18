from django.urls import path
from .views import RegisterView,LoginView,CampaignList,LogoutView,CampaignView,DonationView,DonationList,getCampaign

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('campaignlist/',CampaignList.as_view(),name='campaignlist'),
    path('campaign/',CampaignView.as_view(),name='campaign'),
    path('campaign/<int:pk>/',CampaignView.as_view(),name='campaign_edit_delete'),
    path('donation/',DonationView.as_view(),name='donation'),
    path('donationlist/',DonationList.as_view(),name='donationlist'),
    path('donation/<int:pk>/',DonationView.as_view(),name='donation_edit_delete'),
    path('getcampaign/<int:pk>/',getCampaign.as_view(),name="getcampaign")

]
