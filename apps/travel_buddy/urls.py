from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^main$', views.login_registration, name='tb_login_registration'),
	url(r'^login/process$', views.login_process, name='tb_login_process'),
	url(r'^register/process$', views.registration_process, name='tb_registration_process'),
	# show all travels
	url(r'^travels$', views.show_travels, name='tb_show_travels'),
	url(r'^travel/add$', views.add_travel, name='tb_add_travel'),
	url(r'^travel/add/process$', views.add_travel_process, name='tb_add_travel_process'),
	# click on a trip and see its details
	url(r'^travel/destination/(?P<dest_id>\d+)$', views.show_detail, name='tb_show_detail'),
	# add a travel to self
	url(r'^travel/join/destination/(?P<dest_id>\d+)$', views.join_travel, name='tb_join_travel'),
	url(r'^logout$', views.logout, name='tb_logout')
]