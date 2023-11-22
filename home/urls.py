from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls, name='admin'),
    path('car_details/<int:car_id>/', views.car_details, name='car_details'),
    path('feedback/', views.feedbackurl, name='feedback'),
    path('main/', views.copyindex, name='main'),
    path('submit_form/', views.submit_form, name='submit_form'),
    path('contact/', views.contact, name='contact'),
    path('car-finder/', views.car_finder, name='car-finder'),
    path('news/', views.blog, name='news'),
    path('submit_form_contact/', views.submit_contact_modal_form, name='submit_contact_modal_form'),
    path('submit_carfinder_modal_form/', views.submit_carfinder_modal_form, name='submit_carfinder_modal_form'),  # Added this line
    path('sold/', views.sold_cars, name="sold"),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('about/', views.about, name='about')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
