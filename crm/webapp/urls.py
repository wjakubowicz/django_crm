from django.urls import path
from . import views
from django.urls import include
from two_factor.urls import urlpatterns as tf_urls

urlpatterns = [
    path('', views.home, name=''),

    path('register', views.register, name='register'),
    path('user_login', views.user_login, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
	
    path('', include(tf_urls)),

    path('dashboard', views.dashboard, name='dashboard'),
    
    path('create_record', views.create_record, name='create_record'),
    path('update_record/<int:pk>', views.update_record, name='update_record'),
    path('record/<int:pk>', views.view_record, name='view_record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
	
    path('update-coordinates/', views.update_record_coordinates, name='update_coordinates'),
    
    path('change_theme/', views.change_theme, name='change_theme'),
	
    path('view_map/', views.view_map, name='view_map'),
	
    path('import_data/', views.import_data, name='import_data'),
    path('export_data/', views.export_data, name='export_data'),
	
    path('nominatim-search/', views.nominatim_search, name='nominatim_search'),
]