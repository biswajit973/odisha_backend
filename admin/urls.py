
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
   
    path('auth/superadmin-login/', views.SuperAdminLoginView.as_view(), name='superadmin-login'),
    path('auth/create-admin/', views.CreateAdminAPIView.as_view(), name='create-admin'),
    path('auth/superadmin-logout/', views.LogoutView.as_view(), name='superadmin-logout'),
    path('auth/list-admin/', views.AdminListAPIView.as_view(), name='list-admin'),
    path('auth/delete-admin/<int:pk>/', views.DeleteAdminAPIView.as_view(), name='delete-admin'),
    path('auth/admin-login/', views.AdminLoginView.as_view(), name='admin-login'),
    path('auth/admin-logout/', views.LogoutView.as_view(), name='admin-logout'),
    path('waste_mgmt/list/', views.RequestsListView.as_view(), name='api/waste_mgmt/list/'),
    path('api/admin/waste-mgmt/bookings/<int:booking_id>/', views.AdminUpdateRequestStatusView.as_view(), name='api/admin/waste-mgmt/bookings/<int:booking_id>/'),
    path('api/complaint_mgmt/admin/view/', views.AdminComplaintView.as_view(), name='admin-view-complaintreports'),
    path('api/complaint_mgmt/admin/update-status/<int:pk>/', views.AdminUpdateComplaintReportStatusView.as_view(), name='complaint-update-status'),

    path('api/admin/event_klm/bookings/', views.AdminListAllBookingsView.as_view(), name='api/admin/event_klm/bookings/'),
    path('api/admin/event_klm/bookings/<int:booking_id>/', views.AdminUpdateMandapBookingStatusView.as_view(), name='api/admin/event_klm/bookings/<int:booking_id>/'),

    
    
    

   
    
    
    
    
    
]



if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)      
        