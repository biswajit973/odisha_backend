from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Kalyanmandap)
admin.site.register(Kalyanmandap_booking)
admin.site.register(Requests)
admin.site.register(Request_images)
admin.site.register(Kalyanmandap_images)
admin.site.register(User)
# admin.site.register(StatusUpdates)

admin.site.register(Complaint)
admin.site.register(ComplaintCategory)
admin.site.register(ComplaintSubCategory)
admin.site.register(Complaint_images)
admin.site.register(PromotionalBanners)
admin.site.register(CesspoolRequest)
admin.site.register(CesspoolRequest_images)
admin.site.register(Notification)
admin.site.register(AdminNotifications)





    