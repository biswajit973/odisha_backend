
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
      
      
    path('auth/admin-login/', views.AdminLoginView.as_view(), name='admin-login'),
    path('auth/create-admin/', views.CreateAdminAPIView.as_view(), name='create-admin'),
    path('auth/admin-logout/', views.LogoutView.as_view(), name='admin-logout'),
    path('auth/list-admin/', views.AdminListAPIView.as_view(), name='list-admin'),
    path('auth/delete-admin/<int:pk>/', views.DeleteAdminAPIView.as_view(), name='delete-admin'),
    path('auth/update-admin/<int:pk>/',views.UpdateAdminView.as_view(),name='update-admin'),
        
    path('waste_mgmt/list/', views.RequestsListView.as_view(), name='waste_mgmt/list/'),
    path('waste-mgmt/bookings/<int:booking_id>/', views.AdminUpdateRequestStatusView.as_view(), name='waste-mgmt/bookings/<int:booking_id>/'),
    path('complaint_mgmt/admin/view/', views.AdminComplaintView.as_view(), name='admin-view-complaintreports'),
    path('complaint_mgmt/admin/update-status/<int:pk>/', views.AdminUpdateComplaintReportStatusView.as_view(), name='complaint-update-status'),

    path('event_klm/bookings/', views.AdminListAllBookingsView.as_view(), name='event_klm/bookings/'),
    path('event_klm/bookings/<int:booking_id>/', views.AdminUpdateMandapBookingStatusView.as_view(), name='event_klm/bookings/<int:booking_id>/'),
    
    path('cesspool_mgmt/admin/view/', views.AdminCesspoolrequestsView.as_view(), name='admin-view-cesspoolrequest'),
    # path('cesspool_mgmt/admin/report/<int:pk>/',views.AdminEachCesspoolrequestview.as_view(),name="admin-each-cesspool-request"),
    path('cesspool_mgmt/admin/update-status/<int:pk>/',views.AdminUpdateCesspoolRequestStatus.as_view(), name='cesspoolrequest-update-status'),
    
    path('createbanner/',views.CreateBannerView.as_view(), name='create-banners'),
    path('deletebanner/<int:pk>/',views.DeleteBannerView.as_view(), name='delete-banner'),
    path('updatebanner/<int:pk>/',views.UpdateBannerView.as_view(), name='update-banner'),

    path('event_klm/mandaps/', views.AdminCreateKalyanmandapView.as_view(), name='api/admin/event_klm/mandaps/'),
    
    path('event_klm/viewmandaps/', views.AllKalyanmandapView.as_view(), name='api/admin/event_klm/viewmandaps/'),
    path('event_klm/mandaps/<int:pk>/', views.AdminUpdateKalyanmandapView.as_view(), name='event_klm/mandaps/<int:pk>/'),

    path('event_klm/delete-mandap/<int:pk>/', views.AdminDeleteMandapView.as_view(), name='event_klm/delete-mandap/<int:pk>/        '),

    path('event_klm/mandap-status/<int:pk>/', views.AdminUpdateKalyanmandapStatusView.as_view(), name='event_klm/mandaps/<int:pk>/'),

        path('admin-notifications/', views.AdminNotificationsView.as_view(), name='admin-notifications/'),
        path('filter-admin-notifications/<str:department>/', views.FilterAdminNotificationsView.as_view(), name='filter-admin-notifications/'),

          path('clear-admin-notifications/', views.ClearAdminNotifications.as_view(), name='clear-admin-notifications'),



]



if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)      

        