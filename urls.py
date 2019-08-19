from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^wedding_organizer_app$', views.wedding_organizer_app, name='wedding_organizer_app'),
	url(r'^wedding_organizer_app/wedding_organizer_app_management$', views.wedding_organizer_app_management,
		name='wedding_organizer_app_management'),
	url(r'^new_wedding', views.new_wedding, name='new_wedding'),
	url(r'^wedding_organizer_app_management', views.wedding_organizer_app_management, name='wedding_organizer_app_management'),
	url(r'^add_guest', views.add_guest, name='add_guest'),
	url(r'^add_table', views.add_table, name='add_table'),
	url(r'^generate_halls', views.generate_halls, name='generate_halls'),
]