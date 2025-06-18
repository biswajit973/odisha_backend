from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from .models import *

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirmpassword = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name','email', 'dob', 'address', 'pincode', 'password', 'confirmpassword')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value

    def validate(self, data):
        if data['password'] != data['confirmpassword']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = validated_data.get('email')
        dob = validated_data.get('dob')
        address = validated_data.get('address')
        pincode = validated_data.get('pincode')
        password = validated_data.get('password')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            dob=dob,
            address=address,
            pincode=pincode,
            password=password
        )

        return user
    
class AdminLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    



class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    
    def validate_email(self,value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist")
        return value
    
    
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'dob', 'address', 'pincode']
        
class updateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'dob', 'address', 'pincode']
            
        
class Kalyanmandap_imagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kalyanmandap_images
        fields = ['image']
        
class KalyanmandapSerializer(serializers.ModelSerializer):
    active = serializers.BooleanField(required=False, default=True)
    
    class Meta:
        model = Kalyanmandap
        fields = '__all__'        


class Request_imagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request_images
        fields = ['image']

class RequestSerializer(serializers.ModelSerializer):
    request_images = Request_imagesSerializer(many=True, read_only=True)
    waste_type_other = serializers.CharField(required=False, allow_blank=True)
    time_slot = serializers.CharField(required=False, allow_blank=True)
    date= serializers.DateField(required=False, allow_null=True)
    house_number = serializers.CharField(required=False, allow_blank=True)
    floor= serializers.CharField(required=False, allow_blank=True) 
    block= serializers.CharField(required=False, allow_blank=True)
    landmark= serializers.CharField(required=False, allow_blank=True)
    address= serializers.CharField(required=False, allow_blank=True)
    payment_method = serializers.CharField(required=False, allow_blank=True)
    comment = serializers.CharField(required=False, allow_blank=True)
    payment_amount =serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Requests
        fields = ['id','booking_id','service_type','type', 'description', 'waste_type', 'address','waste_type_other', 'date','house_number','floor','block','landmark','location', 'contact_number', 'time_slot', 'payment_method','payment_amount','payment_status','request_images', 'status', 'comment']

    


class RequestsListSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = Requests
        fields = '__all__'
    def get_user_name(self, obj):
     return f"{obj.user.first_name} {obj.user.last_name}".strip()
        
        
class UserRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests
        fields = '__all__'
        
class EachRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests
        fields = '__all__'
        
                
        
class KalyanmandapBookingSerializer(serializers.ModelSerializer):
    mandap_name = serializers.CharField(source='kalyanmandap.mandap_name', read_only=True)
    mandap_description = serializers.CharField(source='kalyanmandap.mandap_description', read_only=True)
    mandap_address = serializers.CharField(source='kalyanmandap.mandap_address', read_only=True)
    mandap_contact_number = serializers.CharField(source='kalyanmandap.mandap_contact_number', read_only=True)
    mandap_capacity = serializers.CharField(source='kalyanmandap.mandap_capacity', read_only=True)
    mandap_amenities =serializers.CharField(source='kalyanmandap.mandap_amenities', read_only=True)
    mandap_minimum_booking_unit = serializers.CharField(source='kalyanmandap.mandap_minimum_booking_unit', read_only=True)
    mandap_price_range = serializers.CharField(source='kalyanmandap.mandamandap_price_rangep_name', read_only=True)
    mandap_price_note = serializers.CharField(source='kalyanmandap.mandap_price_note', read_only=True)
    kalyanmandap_images = serializers.SerializerMethodField()
    class Meta:
        model = Kalyanmandap_booking
        fields = ['id','booking_id','service_type','kalyanmandap','mandap_name','occasion','number_of_people','start_datetime','end_datetime','duration',
                  'additional_requests','payment_method','status','comment','payment_amount','payment_status',
                  'mandap_description','mandap_address','mandap_contact_number','mandap_capacity','mandap_amenities',
                  'mandap_minimum_booking_unit','mandap_price_range','mandap_price_note','kalyanmandap_images']   
             
    def get_kalyanmandap_images(self, obj):
        images = obj.kalyanmandap.kalyanmandap_images.all()
        return Kalyanmandap_imagesSerializer(images, many=True, context=self.context).data    

# class AdminKalyanmandapBookingSerializer(serializers.ModelSerializer):
#     user_name = serializers.SerializerMethodField()
#     mandap_name = serializers.CharField(source='kalyanmandap.mandap_name', read_only=True)
#     mandap_description = serializers.CharField(source='kalyanmandap.mandap_description', read_only=True)
#     mandap_address = serializers.CharField(source='kalyanmandap.mandap_address', read_only=True)
#     mandap_contact_number = serializers.CharField(source='kalyanmandap.mandap_contact_number', read_only=True)
#     mandap_capacity = serializers.CharField(source='kalyanmandap.mandap_capacity', read_only=True)
#     mandap_amenities =serializers.CharField(source='kalyanmandap.mandap_amenities', read_only=True)
#     mandap_minimum_booking_unit = serializers.CharField(source='kalyanmandap.mandap_minimum_booking_unit', read_only=True)
#     mandap_price_range = serializers.CharField(source='kalyanmandap.mandamandap_price_rangep_name', read_only=True)
#     mandap_price_note = serializers.CharField(source='kalyanmandap.mandap_price_note', read_only=True)
#     kalyanmandap_images = serializers.SerializerMethodField()
#     class Meta:
#         model = Kalyanmandap_booking
#         fields = ['id','booking_id','user_name','service_type','kalyanmandap','mandap_name','occasion','number_of_people','start_datetime','end_datetime','duration',
#                   'additional_requests','payment_method','status','comment'
#                   ,'mandap_description','mandap_address','mandap_contact_number','mandap_capacity','mandap_amenities',
#                   'mandap_minimum_booking_unit','mandap_price_range','mandap_price_note','kalyanmandap_images']   
             
#     def get_kalyanmandap_images(self, obj):
#         images = obj.kalyanmandap.kalyanmandap_images.all()
#         return Kalyanmandap_imagesSerializer(images, many=True, context=self.context).data    
#     def get_user_name(self, obj):
#         return f"{obj.user.first_name} {obj.user.last_name}".strip()



       
        

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
    custom_category =  serializers.CharField(required=False, allow_blank=True)
    user_name = serializers.SerializerMethodField()

    category_name = serializers.SerializerMethodField()
    subcategory_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Complaint
        fields = ['id','booking_id','category','user_name', 'service_type','subcategory','description','category_name','subcategory_name','custom_category', 'location','address', 'status', 'comment','complaint_images']
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
        fields = ['id','booking_id','name','service_type', 'contact_number','location','address','description','waste_tank_type','capacity','urgency_level','preferred_datetime','accessibility_note','status','comment','payment_amount','payment_status','cesspool_images']



class CessPoolStatusUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model =  CesspoolRequest
        fields = ["status","comment"]
            
class BannerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PromotionalBanners
        fields=['id','hyperlink','description','banner_image']            



# serializers.py



class NotificationSerializer(serializers.ModelSerializer):
    
    notification_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = ['notification_count','id','booking_id', 'title', 'status', 'comment','payment_status','payment_amount','created_at','category','service_type']
    
    def get_notification_count(self,obj):
        return Notification.objects.filter(user=obj.user).count()
    
    
