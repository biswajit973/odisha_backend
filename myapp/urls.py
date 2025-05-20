
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    path('api/auth/register/', views.RegisterView.as_view(), name='register'),
    path('api/auth/login/', views.LoginView.as_view(), name='login'),
    path('api/auth/admin-login/', views.AdminLoginView.as_view(), name='admin-login'),
    path('api/auth/admin-logout/', views.AdminLogoutView.as_view(), name='admin-logout'),
    path('api/auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reset-password_api/', views.ResetPasswordRequestView.as_view(), name='reset_password_request_api'),
    path('reset-password_api/confirm/', views.PasswordResetView.as_view(), name='reset_password_confirm_api'),
    path('api/account-details/', views.AccountDetails.as_view(), name='account_details'),
    path('api/waste_mgmt/create/', views.CreateRequestView.as_view(), name='api/waste_mgmt/create/'),
    path('api/waste_mgmt/list/', views.RequestsListView.as_view(), name='api/waste_mgmt/list/'),
    path('api/waste_mgmt/user-requests/', views.UserRequestsView.as_view(), name='api/waste_mgmt/user-requests/'),
    path('api/waste_mgmt/<int:pk>/', views.EachUserRequestView.as_view(), name='api/waste_mgmt/each-request/'),
    path('api/admin/waste_mgmt/public-waste-count/', views.PublicWasteRequestCountView.as_view(), name='api/admin/waste_mgmt/public-waste-count/'),
    path('api/admin/waste_mgmt/personal-waste-count/', views.PersonalWasteRequestCountView.as_view(), name='api/admin/waste_mgmt/personal-waste-count/'),
    path('api/admin/waste_mgmt/public-waste-list/', views.RequestsPublicWasteListView.as_view(), name='api/admin/waste_mgmt/public-waste-list/'),
    path('api/admin/waste_mgmt/personal-waste-list/', views.RequestsPersonalWasteListView.as_view(), name='api/admin/waste_mgmt/personal-waste-list/'),
    path('api/waste_mgmt/<int:pk>/status/', views.StatusUpdateView.as_view(), name='api/waste_mgmt/<int:pk>/status/'),
    path('api/admin/event_klm/mandaps/', views.AdminCreateKalyanmandapView.as_view(), name='api/admin/event_klm/mandaps/'),
    path('api/event_klm/mandaps/', views.GetKalyanmandapView.as_view(), name='api//event_klm/mandaps/'), 
    path('api/admin/event_klm/mandaps/<int:pk>/', views.AdminUpdateKalyanmandapView.as_view(), name='api/admin/event_klm/mandaps/<int:pk>/'),
    path('api/event_klm/mandaps/<int:pk>/', views.GetOneKalyanmandapView.as_view(), name='api/event_klm/mandaps/<int:pk>/'),
    path('api/event_klm/book/', views.BookKalyanmandapView.as_view(), name='api/event_klm/book/'),
    path('api/admin/event_klm/bookings/', views.AdminListAllBookingsView.as_view(), name='api/admin/event_klm/bookings/'),
    path('api/event_klm/bookings/', views.UserKalyanmandapBookingsView.as_view(), name='api/user/event_klm/bookings/'),
    path('api/admin/event_klm/bookings/<int:booking_id>/', views.AdminUpdateBookingStatusView.as_view(), name='api/admin/event_klm/bookings/<int:booking_id>/'),
]



if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)      
        