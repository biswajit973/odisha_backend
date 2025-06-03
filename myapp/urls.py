
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    path('api/auth/register/', views.RegisterView.as_view(), name='register'),
    path('api/auth/login/', views.LoginView.as_view(), name='login'),
   
    path('api/auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/send-password-reset-otp/', views.PasswordResetOTPView.as_view(), name='send-password-reset-otp'),
    path('api/auth/resend-password-reset-otp/', views.ResendPasswordResetOTPView.as_view(), name='resend-password-reset-otp'),
    path('api/auth/verify-password-reset-otp/',views.VerifyOTPView.as_view(),name="verify-password-reset-otp"),
    
    path('api/auth/reset-password/', views.PasswordResetView.as_view(), name='reset-password'),
    path('api/account-details/', views.AccountDetails.as_view(), name='account_details'),
    path('api/updateaccount-details/', views.UpdateUserProfileView.as_view(), name='updateaccount_details'),
    path('api/waste_mgmt/create/', views.CreateRequestView.as_view(), name='api/waste_mgmt/create/'),
    path('api/waste_mgmt/list/', views.RequestsListView.as_view(), name='api/waste_mgmt/list/'),
    path('api/waste_mgmt/user-requests/', views.UserRequestsView.as_view(), name='api/waste_mgmt/user-requests/'),
    path('api/waste_mgmt/user-request/<int:pk>/',views.UserEachRequestView.as_view(), name='api/waste_mgmt/user-request/'),

    
    path('api/waste_mgmt/<int:pk>/', views.EachRequestView.as_view(), name='api/waste_mgmt/each-request/'),
    path('api/admin/waste_mgmt/public-waste-count/', views.PublicWasteRequestCountView.as_view(), name='api/admin/waste_mgmt/public-waste-count/'),
    path('api/admin/waste_mgmt/personal-waste-count/', views.PersonalWasteRequestCountView.as_view(), name='api/admin/waste_mgmt/personal-waste-count/'),
    path('api/admin/waste_mgmt/public-waste-list/', views.RequestsPublicWasteListView.as_view(), name='api/admin/waste_mgmt/public-waste-list/'),
    path('api/admin/waste_mgmt/personal-waste-list/', views.RequestsPersonalWasteListView.as_view(), name='api/admin/waste_mgmt/personal-waste-list/'),
    path('api/user/bookings/', views.UserBookingsView.as_view(), name='api/user/bookings/'),
    path('api/user/eachbooking/', views.UserEachBookingView.as_view(), name='api/user/eachbooking/'),
    path('api/admin/event_klm/mandaps/', views.AdminCreateKalyanmandapView.as_view(), name='api/admin/event_klm/mandaps/'),
    path('api/event_klm/mandaps/', views.GetKalyanmandapView.as_view(), name='api//event_klm/mandaps/'), 
    path('api/admin/event_klm/mandaps/<int:pk>/', views.AdminUpdateKalyanmandapView.as_view(), name='api/admin/event_klm/mandaps/<int:pk>/'),
    path('api/event_klm/mandaps/<int:pk>/', views.GetOneKalyanmandapView.as_view(), name='api/event_klm/mandaps/<int:pk>/'),
    path('api/event_klm/book/', views.BookKalyanmandapView.as_view(), name='api/event_klm/book/'),
    path('api/admin/event_klm/bookings/', views.AdminListAllBookingsView.as_view(), name='api/admin/event_klm/bookings/'),
    path('api/admin/event_klm/booking/<int:pk>/', views.AdminEachMandapBookingView.as_view(), name='api/admin/event_klm/eachbooking/'),

    path('api/event_klm/bookings/', views.UserKalyanmandapBookingsView.as_view(), name='api/user/event_klm/bookings/'),
    path('api/event_klm/bookings/<int:pk>/', views.UserEachKalyanmandapBookingView.as_view(), name='api/user/event_klm/eachbooking/'),

    path('api/admin/event_klm/bookings/<int:booking_id>/', views.AdminUpdateMandapBookingStatusView.as_view(), name='api/admin/event_klm/bookings/<int:booking_id>/'),
    path('api/admin/waste-mgmt/bookings/<int:booking_id>/', views.AdminUpdateRequestStatusView.as_view(), name='api/admin/waste-mgmt/bookings/<int:booking_id>/'),
    path('api/pollution_mgmt/categories/', views.PollutionCategoryView.as_view(), name='pollution-categories'),
    path('api/pollution_mgmt/create/', views.CreateReportView.as_view(), name='user-submit-report'),
    path('api/pollution_mgmt/my-reports/', views.UserReportsView.as_view(), name='user-reports'),
    path('api/pollution_mgmt/my-report/<int:pk>/', views.UserEachReportView.as_view(), name='user-report'),
    path('api/pollution_mgmt/admin/view/', views.AdminReportView.as_view(), name='admin-view-reports'),
    path('api/pollution_mgmt/admin/report/<int:pk>/',views.AdminEachReportView.as_view(),name="admin-each-report"),
    path('api/pollution_mgmt/admin/update-status/<int:pk>/', views.AdminUpdateReportStatusView.as_view(), name='pollution-update-status'),
    path('api/complaint_mgmt/categories/', views.ComplaintCategoryView.as_view(), name='pollution-categories'),
    path('api/complaint_mgmt/create/', views.CreateComplaintView.as_view(), name='user-submit-complaintreport'),
    path('api/complaint_mgmt/my-reports/', views.UserComplaintsView.as_view(), name='user-complaintreports'),
    path('api/complaint_mgmt/my-report/<int:pk>/', views.UserEachComplaintView.as_view(), name='user-complaintreport'),
    path('api/complaint_mgmt/admin/view/', views.AdminComplaintView.as_view(), name='admin-view-complaintreports'),
    path('api/complaint_mgmt/admin/report/<int:pk>/',views.AdminEachComplaintReportView.as_view(),name="admin-each-complaint-report"),
    path('api/complaint_mgmt/admin/update-status/<int:pk>/', views.AdminUpdateComplaintReportStatusView.as_view(), name='complaint-update-status'),
    
    path('api/cesspool_mgmt/create/', views.CreateCesspoolRequestView.as_view(), name='user-submit-cesspoolrequest'),
    path('api/cesspool_mgmt/my-requests/', views.UserCesspoolRequests.as_view(), name='user-cesspoolrequests'),
    path('api/cesspool_mgmt/my-request/<int:pk>/', views.UserCesspoolEachRequest.as_view(), name='user-cesspoolrequest'),
    path('api/cesspool_mgmt/admin/view/', views.AdminCesspoolrequestsView.as_view(), name='admin-view-cesspoolrequest'),
    path('api/cesspool_mgmt/admin/report/<int:pk>/',views.AdminEachCesspoolrequestview.as_view(),name="admin-each-cesspool-request"),
    path('api/cesspool_mgmt/admin/update-status/<int:pk>/',views.AdminUpdateCesspoolRequestStatus.as_view(), name='cesspoolrequest-update-status'),
    path('api/banners/',views.BannersView.as_view(), name='banners'),
    path('api/admin/createbanner/',views.CreateBannerView.as_view(), name='create-banners'),
    path('api/admin/deletebanner/<int:pk>/',views.DeleteBannerView.as_view(), name='delete-banner'),
    path('api/admin/updatebanner/<int:pk>/',views.UpdateBannerView.as_view(), name='update-banner'),
    

   

    path('api/auth/send-otp/', views.SendOTPView.as_view(), name='send-otp'),
    path('api/auth/resend-otp/', views.resendOTPview.as_view(), name='resendotp'),
    path('api/auth/verify-otp/',views.VerifyOTPView.as_view(),name="verify-otp"),
    
    
    
    
    
]



if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)      
        