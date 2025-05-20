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
    
    
class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self,value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist")
        return value


class PasswordResetSerializer(serializers.Serializer):
    uid  = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    
    
    
class UserProfileSerializer(serializers.ModelSerializer):
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
    payment_status = serializers.BooleanField(required=False, default=False)
    time_slot = serializers.CharField(required=False, allow_blank=True)
    date= serializers.DateField(required=False, allow_null=True)
    house_number = serializers.CharField(required=False, allow_blank=True)
    floor= serializers.CharField(required=False, allow_blank=True) 
    block= serializers.CharField(required=False, allow_blank=True)
    landmark= serializers.CharField(required=False, allow_blank=True)
    address= serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Requests
        fields = ['type', 'description', 'waste_type', 'address','waste_type_other', 'date','house_number','floor','block','landmark','location', 'contact_number', 'time_slot', 'payment_method', 'payment_status', 'request_images']

    


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
        
        


class StatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusUpdates
        fields = ['status', 'comment']
        
        
        
class KalyanmandapBookingSerializer(serializers.ModelSerializer):
    mandap_name = serializers.CharField(source='kalyanmandap.mandap_name', read_only=True)
    class Meta:
        model = Kalyanmandap_booking
        fields = ['id','kalyanmandap','mandap_name','occasion','number_of_people','start_datetime','end_datetime','duration','additional_requests','payment_method','status']        
        

class AdminKalyanmandapBookingSerializer(serializers.ModelSerializer):
    mandap_name = serializers.CharField(source='kalyanmandap.mandap_name', read_only=True)
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = Kalyanmandap_booking
        fields = ['id','kalyanmandap','mandap_name','user','user_name','occasion','number_of_people','start_datetime','end_datetime','duration','additional_requests','payment_method','status']        
    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip()



class BookingStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kalyanmandap_booking
        fields = ['status']

    

