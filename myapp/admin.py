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
admin.site.register(PollutionTypeMaster)
admin.site.register(PollutionReport)
admin.site.register(PollutionSubCategory)
admin.site.register(Pollution_images)



    