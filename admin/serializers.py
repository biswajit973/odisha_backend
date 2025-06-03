from rest_framework import serializers
from django.contrib.auth import get_user_model

from myapp.models import *

User = get_user_model()
class AdminLoginSerializer(serializers.Serializer):
  
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class SuperAdminLoginSerializer(serializers.Serializer):
     email = serializers.CharField(required=True)
     password = serializers.CharField(required=True, write_only=True)
    


class CreateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'role', 'department']


class AdminListSerializer(serializers.ModelSerializer):
    
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'role', 'department','full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    
class RequestsListSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = Requests
        fields = '__all__'
    def get_user_name(self, obj):
     return f"{obj.user.first_name} {obj.user.last_name}".strip()    


class RequestStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests
        fields = ['status','comment']  




class ComplaintSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintSubCategory
        fields = ['id', 'name']

class ComplaintCategorySerializer(serializers.ModelSerializer):
    subcategories = ComplaintSubCategorySerializer(many=True, read_only=True)

    class Meta:
        model =  ComplaintCategory
        fields = ['id', 'name', 'subcategories']
        
        
class Complaint_imagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint_images
        fields = ['image']        

class ComplaintSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(required=False, allow_blank=True)
    complaint_images = Complaint_imagesSerializer(many=True, read_only=True)
    custom_subcategory =  serializers.CharField(required=False, allow_blank=True)
    user_name = serializers.SerializerMethodField()

    category_name = serializers.SerializerMethodField()
    subcategory_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Complaint
        fields = ['id','category','user_name', 'service_type','subcategory', 'description','category_name','subcategory_name','custom_subcategory', 'location','address', 'status', 'comment','complaint_images']
    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip()
    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    def get_subcategory_name(self, obj):
        return obj.subcategory.name if obj.subcategory else None


class ComplaintReportStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ['status','comment']        



class CesspoolRequest_imagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CesspoolRequest_images
        fields =['image']

class CesspoolRequestSerializer(serializers.ModelSerializer):
    
    cesspool_images = CesspoolRequest_imagesSerializer(many=True,read_only=True)
    comment = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model =  CesspoolRequest
        fields = ['id','name','service_type', 'contact_number','location','address','description','waste_tank_type','capacity','urgency_level','preferred_datetime','accessibility_note','status','comment','cesspool_images']



class CessPoolStatusUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model =  CesspoolRequest
        fields = ["status","comment"]   
        
         

class Kalyanmandap_imagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kalyanmandap_images
        fields = ['image']
        
class KalyanmandapSerializer(serializers.ModelSerializer):
    active = serializers.BooleanField(required=False, default=True)
    
    class Meta:
        model = Kalyanmandap
        fields = '__all__'  

class AdminKalyanmandapBookingSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    mandap_name = serializers.CharField(source='kalyanmandap.mandap_name', read_only=True)
    mandap_description = serializers.CharField(source='kalyanmandap.mandap_description', read_only=True)
    mandap_address = serializers.CharField(source='kalyanmandap.mandap_address', read_only=True)
    mandap_contact_number = serializers.CharField(source='kalyanmandap.mandap_contact_number', read_only=True)
    mandap_capacity = serializers.CharField(source='kalyanmandap.mandap_capacity', read_only=True)
    mandap_amenities =serializers.CharField(source='kalyanmandap.mandap_amenities', read_only=True)
    mandap_minimum_booking_unit = serializers.CharField(source='kalyanmandap.mandap_minimum_booking_unit', read_only=True)
    mandap_price_range = serializers.CharField(source='kalyanmandap.mandap_price_range', read_only=True)
    mandap_price_note = serializers.CharField(source='kalyanmandap.mandap_price_note', read_only=True)
    kalyanmandap_images = serializers.SerializerMethodField()
    class Meta:
        model = Kalyanmandap_booking
        fields = ['id','user_name','service_type','kalyanmandap','mandap_name','occasion','number_of_people','start_datetime','end_datetime','duration',
                  'additional_requests','payment_method','status','comment'
                  ,'mandap_description','mandap_address','mandap_contact_number','mandap_capacity','mandap_amenities',
                  'mandap_minimum_booking_unit','mandap_price_range','mandap_price_note','kalyanmandap_images']   
             
    def get_kalyanmandap_images(self, obj):
        images = obj.kalyanmandap.kalyanmandap_images.all()
        return Kalyanmandap_imagesSerializer(images, many=True, context=self.context).data    
    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip()



class MandapBookingStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kalyanmandap_booking
        fields = ['status','comment']            