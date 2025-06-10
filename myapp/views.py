import random
from django.shortcuts import render

from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from datetime import timedelta
from django.utils import timezone
from allauth.socialaccount.models import SocialAccount
import pyotp

from django.contrib.auth import get_user_model

from adminapp.models import *


User = get_user_model()


class SendOTPView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            email = request.data.get('email')
            
            if User.objects.filter(email=email).exists():
                
                return Response({"message": "Email Already Exists"},status=status.HTTP_400_BAD_REQUEST)
            
            secret_key = pyotp.random_base32()
            totp = pyotp.TOTP(secret_key, interval=300)
            otp_value = totp.now()
            print(otp_value)
        

            send_mail(
                subject='Email Verification Code from Joda Municipality',
                message=(
                    f'Dear User,\n\n'
                    f'To verify your email address, please use the following One-Time Password (OTP):\n\n'
                    f'{otp_value}\n\n'
                    f'This code is valid for 5 minutes.\n\n'
                    f'If you did not request this verification, please ignore this email.\n\n'
                    f'Thank you,\n'
                    
                ),
                from_email='jodamunicipality@gmail.com',
                recipient_list=[email],
                fail_silently=False,
            )

            return Response({'message': 'OTP sent to email', "secret_key":secret_key}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': 'Failed to send OTP email', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class resendOTPview(APIView):
    permission_classes = []
    def post(self, request):
        try:
            email = request.data.get('email')
            secret_key = request.data.get('secret_key')
            totp = pyotp.TOTP(secret_key, interval=300)
            otp_value = totp.now()
            print(otp_value)
        

            send_mail(
                subject='Email Verification Code from Joda Municipality',
                message=(
                    f'Dear User,\n\n'
                    f'To verify your email address, please use the following One-Time Password (OTP):\n\n'
                    f'{otp_value}\n\n'
                    f'This code is valid for 5 minutes.\n\n'
                    f'If you did not request this verification, please ignore this email.\n\n'
                    f'Thank you,\n'
                    
                ),
                from_email='jodamunicipality@gmail.com',
                recipient_list=[email],
                fail_silently=False,
            )

            return Response({'message': 'OTP resent to email'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': 'Failed to send OTP email', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
            
class VerifyOTPView(APIView):
    permission_classes = []

    def post(self, request):
        
        secret_key = request.data.get('secret_key')
        otp_value = request.data.get('otpValue')
        print(otp_value)
        
        veri_otp =pyotp.TOTP(secret_key,interval=300)
        print(secret_key)
        print(veri_otp)
        
        if  not secret_key or not otp_value:
            return Response({'message': 'Missing secret_key, or otpValue'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if veri_otp.verify(otp_value, valid_window=1):
                return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': 'OTP verification failed', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class RegisterView(APIView):
    permission_classes = []

    def post(self,request):
        
        firstname = request.data.get('first_name')
        lastname = request.data.get('last_name')
        email = request.data.get('email')
        fullname = f"{firstname} {lastname}".strip()
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():            
                 serializer.save()
                 send_mail(
                    subject='Registration Successful – Welcome to Joda Municipality',
                    message=(
                        f'Dear { fullname or "User"},\n\n'
                        f'Congratulations! Your registration with Joda Municipality has been completed successfully.\n\n'
                        f'You can now log in using your registered email and password.\n\n'
                        f'If you have any questions or need support, feel free to reply to this email.\n\n'
                        f'Thank you,\n'
                        f'Joda Municipality Team'
                    ),
                    from_email='jodamunicipality@gmail.com',
                    recipient_list=[email],
                    fail_silently=False,
                 )
                 return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
            
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class LoginView(APIView):
    permission_classes = []
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'address': user.address,
            'pincode': user.pincode,
            'dob': user.dob,
            
        })
    


User = get_user_model()


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode   
from django.utils.encoding import force_bytes     
from django.utils.http import urlsafe_base64_decode
        


from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

class PasswordResetOTPView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            email = request.data.get('email')
            user = User.objects.get(email=email)
            if not user :
                return Response({"message": "Email Not Found (or) Invalid Email"}, status=status.HTTP_400_BAD_REQUEST)
            name = user.first_name
            secret_key = pyotp.random_base32()
            totp = pyotp.TOTP(secret_key, interval=300)
            otp_value = totp.now()
            print(otp_value)

            subject = 'Joda Municipality: Password Reset Code'
            
            html_content = f"""
                <html>
                    <body style="font-family: Arial, sans-serif; background-color: #ffffff; color: #000000; padding: 20px;">
                        <div style="max-width: 600px; margin: auto; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden;">
                            <div style="background-color: #000000; color: #ffffff; padding: 20px; text-align: center;">
                                <h2 style="margin: 0;">Joda Municipality</h2>
                            </div>
                            <div style="padding: 20px;">
                                <p style="font-size: 16px;">Dear {name},</p>
                                <p style="font-size: 16px;">
                                    To reset your password, please use the following One-Time Password (OTP):
                                </p>
                                <div style="text-align: center; margin: 20px 0;">
                                    <span style="background-color: #ff6600; color: #ffffff; padding: 10px 20px; font-size: 20px; border-radius: 4px;">
                                        {otp_value}
                                    </span>
                                </div>
                                <p style="font-size: 16px;">
                                    This code is valid for 5 minutes.
                                </p>
                                <p style="font-size: 16px;">
                                    If you did not request this password reset, please ignore this email.
                                </p>
                                <p style="font-size: 16px;">
                                    Thank you,<br/>
                                    <strong>Joda Municipality</strong>
                                </p>
                            </div>
                        </div>
                    </body>
                </html>
            """
            text_content = strip_tags(html_content)

            email_message = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email='jodamunicipality@gmail.com',
                to=[email]
            )
            email_message.attach_alternative(html_content, "text/html")
            email_message.send(fail_silently=False)

            return Response({'message': 'OTP sent to email', "secret_key": secret_key}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': 'Failed to send OTP email', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ResendPasswordResetOTPView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            email = request.data.get('email')
            user = User.objects.get(email=email)
            
            name = user.first_name
            secret_key = request.data.get('secret_key')
            totp = pyotp.TOTP(secret_key, interval=300)
            otp_value = totp.now()
            print(otp_value)
        
            subject = 'Joda Municipality: Password Reset Code'
            
            html_content = f"""
                <html>
                    <body style="font-family: Arial, sans-serif; background-color: #ffffff; color: #000000; padding: 20px;">
                        <div style="max-width: 600px; margin: auto; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden;">
                            <div style="background-color: #000000; color: #ffffff; padding: 20px; text-align: center;">
                                <h2 style="margin: 0;">Joda Municipality</h2>
                            </div>
                            <div style="padding: 20px;">
                                <p style="font-size: 16px;">Dear {name},</p>
                                <p style="font-size: 16px;">
                                    To reset your password, please use the following One-Time Password (OTP):
                                </p>
                                <div style="text-align: center; margin: 20px 0;">
                                    <span style="background-color: #ff6600; color: #ffffff; padding: 10px 20px; font-size: 20px; border-radius: 4px;">
                                        {otp_value}
                                    </span>
                                </div>
                                <p style="font-size: 16px;">
                                    This code is valid for 5 minutes.
                                </p>
                                <p style="font-size: 16px;">
                                    If you did not request this password reset, please ignore this email.
                                </p>
                                <p style="font-size: 16px;">
                                    Thank you,<br/>
                                    <strong>Joda Municipality</strong>
                                </p>
                            </div>
                        </div>
                    </body>
                </html>
            """
            text_content = strip_tags(html_content)

            email_message = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email='jodamunicipality@gmail.com',
                to=[email]
            )
            email_message.attach_alternative(html_content, "text/html")
            email_message.send(fail_silently=False)

            return Response({'message': 'OTP resent to email'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': 'Failed to send OTP email', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
         



class PasswordResetView(APIView):
    permission_classes = []
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        new_password = serializer.validated_data['new_password']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        user.set_password(new_password)
        user.save()

        subject = 'Joda Municipality: Password Reset Successful'
        html_content = f"""
            <html>
                <body style="font-family: Arial, sans-serif; background-color: #ffffff; color: #000000; padding: 20px;">
                    <div style="max-width: 600px; margin: auto; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden;">
                        <div style="background-color: #000000; color: #ffffff; padding: 20px; text-align: center;">
                            <h2 style="margin: 0;">Joda Municipality</h2>
                        </div>
                        <div style="padding: 20px;">
                            <p style="font-size: 16px;">Dear {user.first_name},</p>
                            <p style="font-size: 16px;">
                                This is to confirm that your password has been successfully reset.
                            </p>
                            <div style="text-align: center; margin: 20px 0;">
                                <span style="background-color: #ff6600; color: #ffffff; padding: 10px 20px; font-size: 10px; border-radius: 4px;">
                                    Password Reset Successful
                                </span>
                            </div>
                            <p style="font-size: 16px;">
                                If you did not request this password reset, please contact our support team immediately.
                            </p>
                            <p style="font-size: 16px;">
                                Thank you,<br/>
                                <strong>Joda Municipality</strong>
                            </p>
                        </div>
                    </div>
                </body>
            </html>
        """
        text_content = strip_tags(html_content)

        email_message = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email='jodamunicipality@gmail.com',
            to=[email]
        )
        email_message.attach_alternative(html_content, "text/html")
        email_message.send(fail_silently=False)

        return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)

                

class AccountDetails(APIView):    
    permission_classes=[IsAuthenticated]      
    serializer_class = UserProfileSerializer      

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response({"userDetails":serializer.data}, status=status.HTTP_200_OK)
    
    
class UpdateUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        new_email = request.data.get('email')

        if new_email and User.objects.filter(email=new_email).exclude(id=user.id).exists():
            return Response({"message": "Email already in use by another account."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = updateUserProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CreateRequestView(APIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if not request.FILES.getlist('request_images'):
            return Response({"error": "At least one image is required."}, status=status.HTTP_400_BAD_REQUEST)

        request_instance = serializer.save(user=request.user)
        for image in request.FILES.getlist('request_images'):
            Request_images.objects.create(
                request = request_instance,
                image = image
            )
        
        return Response({"message": "Request created successfully","booking_id":request_instance.booking_id}, status=status.HTTP_201_CREATED)
        
        
        
        
class RequestsListView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class   = RequestsListSerializer
    
    def get(self, request):
        requests = Requests.objects.all()
        if not requests.exists():
          return Response({"message": "No requests found."}, status=status.HTTP_200_OK)
        serializer = self.serializer_class(requests, many=True)
        data=serializer.data
        for request in data:
            request_images = Request_images.objects.filter(request_id=request['id'])
            request['request_images']=[img.image.url for img in request_images]
        return Response(data, status=status.HTTP_200_OK)
    
    
class UserRequestsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = UserRequestsSerializer
    
    def get(self, request):
        requests = Requests.objects.filter(user=request.user)
        if not requests.exists():
          return Response({"message": "No requests found."}, status=status.HTTP_200_OK)
        serializer = self.serializer_class(requests, many=True) 
        data=serializer.data
        for request in data:
            request_images = Request_images.objects.filter(request_id=request['id'])
            request['request_images']=[img.image.url for img in request_images]
        return Response(data, status=status.HTTP_200_OK)
    
class UserEachRequestView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = UserRequestsSerializer
    
    def get(self, request,pk):
        
        try:
            requests = Requests.objects.get(user=request.user,id=pk)
        except Requests.DoesNotExist:
            return Response({"message": "No requests found."}, status=status.HTTP_200_OK)
        serializer = self.serializer_class(requests) 
        data=serializer.data
        request_images = Request_images.objects.filter(request_id=requests.id)
        data['request_images']=[img.image.url for img in request_images]
        return Response(data, status=status.HTTP_200_OK)    


class EachRequestView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class   = EachRequestSerializer
    
    def get(self, request, pk):
        
        requests = Requests.objects.filter(id=pk)
        if not requests.exists():
          return Response({"message": "No requests found."}, status=status.HTTP_200_OK)
        serializer = self.serializer_class(requests,many=True)
        data=serializer.data
        for request in data:
            request_images = Request_images.objects.filter(request_id=request['id'])
            request['request_images']=[img.image.url for img in request_images]
        return Response(data, status=status.HTTP_200_OK)
    
class PublicWasteRequestCountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        count = Requests.objects.filter(type='Public Waste').count()
        return Response({"count": count}, status=status.HTTP_200_OK)
    
class PersonalWasteRequestCountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        count = Requests.objects.filter(type='Private Waste').count()
        return Response({"count": count}, status=status.HTTP_200_OK) 
    
class RequestsPublicWasteListView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class   = RequestsListSerializer

    def get(self, request):
        requests = Requests.objects.filter(type='Public Waste')
        if not requests.exists():
            return Response({"message": "No requests found."}, status=status.HTTP_200_OK)
        
        serializer = self.serializer_class(requests, many=True)
        data = serializer.data

        for request in data:
            request_images = Request_images.objects.filter(request_id=request['id'])
            request['request_images'] = [img.image.url for img in request_images]

        return Response(data, status=status.HTTP_200_OK)

class RequestsPersonalWasteListView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class   = RequestsListSerializer

    def get(self, request):
        requests = Requests.objects.filter(type='Private Waste')
        if not requests.exists():
            return Response({"message": "No requests found."}, status=status.HTTP_200_OK)
        
        serializer = self.serializer_class(requests, many=True)
        data = serializer.data

        for request in data:
            request_images = Request_images.objects.filter(request_id=request['id'])
            request['request_images'] = [img.image.url for img in request_images]

        return Response(data, status=status.HTTP_200_OK)    
        
       


    
class AdminCreateKalyanmandapView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = KalyanmandapSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if not request.FILES.getlist('mandap_images'):
            return Response({"error": "At least one image is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        kalyanmandap_instance = serializer.save()
        for image in request.FILES.getlist('mandap_images'):
            Kalyanmandap_images.objects.create(
                Kalyanmandap = kalyanmandap_instance,
                image = image
            )   
        
        return Response({"message": "Kalyanmandap created successfully"}, status=status.HTTP_201_CREATED)
    
class GetKalyanmandapView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = KalyanmandapSerializer
    
    def get(self, request):
        kalyanmandap = Kalyanmandap.objects.filter(active=True)
        if not kalyanmandap.exists():
          return Response({"message": "No kalyanmandaps found."}, status=status.HTTP_200_OK)
      
        serializer = self.serializer_class(kalyanmandap, many=True)
        data=serializer.data
        for kalyanmandap in data:
            mandap_images = Kalyanmandap_images.objects.filter(Kalyanmandap_id=kalyanmandap['id'])
            kalyanmandap['mandap_images'] = [img.image.url for img in mandap_images]
        return Response(data, status=status.HTTP_200_OK)
    
    
class AdminUpdateKalyanmandapView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = KalyanmandapSerializer

    def put(self, request, pk):
        try:
            kalyanmandap = Kalyanmandap.objects.get(id=pk)
        except Kalyanmandap.DoesNotExist:
            return Response({"error": "Kalyanmandap not found."}, status=status.HTTP_404_NOT_FOUND)

        if not request.FILES.getlist('mandap_images'):
            return Response({"error": "At least one image is required."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(kalyanmandap, data=request.data, partial=True)

        if serializer.is_valid():
            kalyanmandap_instance = serializer.save()

            Kalyanmandap_images.objects.filter(Kalyanmandap=kalyanmandap_instance).delete()
            for image in request.FILES.getlist('mandap_images'):
                Kalyanmandap_images.objects.create(
                    Kalyanmandap=kalyanmandap_instance,
                    image=image
                )

            return Response({"message": "Kalyanmandap details updated successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetOneKalyanmandapView(APIView):
    permission_classes = [AllowAny]
    serializer_class = KalyanmandapSerializer
    
    def get(self, request, pk):
        try:
            kalyanmandap = Kalyanmandap.objects.get(active=True,id=pk)
        except Kalyanmandap.DoesNotExist:
            return Response({"error": "Kalyanmandap not found."}, status=status.HTTP_404_NOT_FOUND)
      
        serializer = self.serializer_class(kalyanmandap)
        data=serializer.data
        mandap_images = Kalyanmandap_images.objects.filter(Kalyanmandap_id=kalyanmandap.id)
        data['mandap_images'] = [img.image.url for img in mandap_images]
        return Response(data, status=status.HTTP_200_OK)
    
    



class BookKalyanmandapView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = KalyanmandapBookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  
            return Response({
                "message": "Kalyanmandap booking submitted successfully.",
                
                "booking": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 


class UserKalyanmandapBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
         bookings = Kalyanmandap_booking.objects.filter(user=request.user).order_by('-start_datetime')
        except Kalyanmandap_booking.DoesNotExist:
             return Response({"message": "No record found"}, status=status.HTTP_200_OK)
        serializer = KalyanmandapBookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserEachKalyanmandapBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request,pk):
        try:
         bookings = Kalyanmandap_booking.objects.get(user=request.user,id=pk)
        except Kalyanmandap_booking.DoesNotExist:
             return Response({"message": "No record found"}, status=status.HTTP_200_OK)
        serializer = KalyanmandapBookingSerializer(bookings)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    
    
    
class AdminListAllBookingsView(APIView):
    permission_classes = [IsAdminUser]  

    def get(self, request):
        bookings = Kalyanmandap_booking.objects.all().order_by('-start_datetime')
        serializer = AdminKalyanmandapBookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    
   
class AdminEachMandapBookingView(APIView):
    permission_classes = [IsAdminUser]  

    def get(self, request,pk):
        try:
            bookings = Kalyanmandap_booking.objects.get(id=pk)
        except Kalyanmandap_booking.DoesNotExist:
            return Response({"message": "No record found"}, status=status.HTTP_200_OK)
        serializer = AdminKalyanmandapBookingSerializer(bookings)
        return Response(serializer.data, status=status.HTTP_200_OK) 
    
           
    
    


# class AdminUpdateMandapBookingStatusView(APIView):
#     permission_classes = [IsAdminUser]

#     def put(self, request, booking_id):
#         try:
#             booking = Kalyanmandap_booking.objects.get(id=booking_id)
#         except Kalyanmandap_booking.DoesNotExist:
#             return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = MandapBookingStatusUpdateSerializer(booking, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'Booking status updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class AdminUpdateRequestStatusView(APIView):
#     permission_classes = [IsAdminUser]

#     def put(self, request, booking_id):
#         try:
#             booking = Requests.objects.get(id=booking_id)
#         except Requests.DoesNotExist:
#             return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = RequestStatusUpdateSerializer(booking, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'Request status updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class UserBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        status_filter = request.query_params.get('status', 'active').lower()
        type_filter = request.query_params.get('type', 'all').lower()

        active_statuses = ['pending', 'scheduled']
        past_statuses = ['rejected','approved','completed']
        status_list = active_statuses if status_filter == 'active' else past_statuses

        results = {}

        if type_filter in ['waste','all']:
            waste_bookings = Requests.objects.filter(
                user=user,
                status__in=status_list
            )
            waste_data = RequestSerializer(waste_bookings, many=True)
            results['waste_bookings'] = waste_data.data

           
        if type_filter in ['mandap', 'all']:
            mandap_bookings = Kalyanmandap_booking.objects.filter(
                user=user,
                status__in=status_list
            ).select_related('kalyanmandap')

            mandap_data = KalyanmandapBookingSerializer(mandap_bookings, many=True)
            results['mandap_bookings'] = mandap_data.data
        
    
        if type_filter in ['complaints', 'all']:
            complaints_all = Complaint.objects.filter(
                user=user,
                status__in=status_list
            )
            complaints_data = ComplaintSerializer(complaints_all, many=True)
            results['complaints_bookings'] = complaints_data.data 
            
        if type_filter in ['cesspool', 'all']:
            cesspool_all = CesspoolRequest.objects.filter(
                user=user,
                status__in=status_list
            )
            cesspool_data = CesspoolRequestSerializer(cesspool_all, many=True)
            results['cesspool_bookings'] = cesspool_data.data        
           

        return Response(results, status=status.HTTP_200_OK)
    


from django.shortcuts import get_object_or_404

class UserEachBookingView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        service_type = request.query_params.get('service_type')
        booking_id = request.query_params.get('id')

        if not service_type or not booking_id:
            return Response(
                {"error": "Missing service_type or id in query parameters."},
                status=status.HTTP_400_BAD_REQUEST
            )

        service_type = service_type.lower()

        if service_type == "waste pickup":
            booking = get_object_or_404(Requests, id=booking_id, service_type=service_type,user=user)
            serializer = RequestSerializer(booking)

        elif service_type == "mandap booking":
            booking = get_object_or_404(
                Kalyanmandap_booking.objects.select_related('kalyanmandap'),
                id=booking_id,
                service_type=service_type,user=user
            )
            serializer = KalyanmandapBookingSerializer(booking)
            
           
        
        elif service_type == "cesspool":
            booking = get_object_or_404(CesspoolRequest, id=booking_id, service_type=service_type,user=user)
            serializer = CesspoolRequestSerializer(booking)  
            
        elif service_type == "complaints":
            booking = get_object_or_404(Complaint, id=booking_id, service_type=service_type,user=user)
            serializer = ComplaintSerializer(booking)            

        else:
            return Response(
                {"error": f"Invalid service_type: {service_type}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    



class ComplaintCategoryView(APIView):
    def get(self, request):
        categories = ComplaintCategory.objects.filter(active_status=True)
        serializer = ComplaintCategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateComplaintView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        images_data = data.pop("complaint_images", [])
        serializer = ComplaintSerializer(data=request.data)
        if not images_data:
            return Response({"error": "At least one image is required."}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            Complaint_instance = serializer.save(user=request.user)
            for img in images_data:
                Complaint_images.objects.create(
                    complaint = Complaint_instance,
                    image = img
                )  
            return Response({"message": "Complaint submitted successfully","booking_id":Complaint_instance.booking_id}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
class UserComplaintsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
         try:
            reports = Complaint.objects.filter(user=request.user)
            serializer = ComplaintSerializer(reports, many=True)
            data = serializer.data
            for complaint in data:
                complaint_images = Complaint_images.objects.filter(complaint_id=complaint['id'])
                complaint['complaint_images']=[img.image.url for img in complaint_images]
            return Response(data, status=status.HTTP_200_OK)
         except Complaint.DoesNotExist:
            return Response({"message": "No records found"}, status=status.HTTP_200_OK)

class UserEachComplaintView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request,pk):
         try:
            report= Complaint.objects.get(user=request.user,id=pk)
            serializer = ComplaintSerializer(report)
            data = serializer.data
            complaint_images = Complaint_images.objects.filter(complaint_id=report.id)
            data['complaint_images']=[img.image.url for img in complaint_images]
            return Response(data, status=status.HTTP_200_OK)
            
         except Complaint.DoesNotExist:
            return Response({"message": "No record found"}, status=status.HTTP_200_OK)        



class AdminComplaintView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        try:
            reports = Complaint.objects.all()
            serializer = ComplaintSerializer(reports,many=True)
            data = serializer.data
            for complaint in data:
                complaint_images = Complaint_images.objects.filter(complaint_id=complaint['id'])
                complaint['complaint_images']=[img.image.url for img in complaint_images]
            return Response(data, status=status.HTTP_200_OK)
        except Complaint.DoesNotExist:
            return Response({"message": "No records found"}, status=status.HTTP_200_OK)

        
    
    
class AdminEachComplaintReportView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, pk):
       try:
            report = Complaint.objects.get(id=pk)
            serializer = ComplaintSerializer(report)
            data = serializer.data
            complaint_images = Complaint_images.objects.filter(complaint_id=report.id)
            data['complaint_images']=[img.image.url for img in complaint_images]
            return Response(data, status=status.HTTP_200_OK)
       except Complaint.DoesNotExist:
            return Response({"message": "No record found"}, status=status.HTTP_200_OK)

class AdminUpdateComplaintReportStatusView(APIView):
    permission_classes = [IsAdminUser]
    def put(self, request, pk):
        report = get_object_or_404(Complaint, pk=pk)
        serializer = ComplaintReportStatusUpdateSerializer(report, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Status updated successfully."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class CreateCesspoolRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        images_data = data.pop("cesspool_images", [])

        serializer = CesspoolRequestSerializer(data=request.data)
        if serializer.is_valid():
            cesspool_instance = serializer.save(user=request.user)

            if not images_data:
                return Response({"message": "At least one image is required"}, status=status.HTTP_400_BAD_REQUEST)

            for img in images_data:
                CesspoolRequest_images.objects.create(Cesspool=cesspool_instance, image=img)

            return Response({"message": "CessPool request raised Successfully","booking_id":cesspool_instance.booking_id}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    
    
class UserCesspoolRequests(APIView):
    
    permission_classes = [IsAuthenticated]
      
    def get(self,request):
        try:
            data = CesspoolRequest.objects.filter(user=request.user)
            serializer = CesspoolRequestSerializer(data,many=True)
            data = serializer.data
            for cesspoolrequest in data:
                cesspool_images = CesspoolRequest_images.objects.filter(Cesspool_id=cesspoolrequest['id'])
                cesspoolrequest['cesspool_images']=[img.image.url for img in cesspool_images]
            return Response(data, status=status.HTTP_200_OK)
        except CesspoolRequest.DoesNotExist:
            return Response({"message": "No record found"}, status=status.HTTP_200_OK)
        
        
class UserCesspoolEachRequest(APIView):
    
    permission_classes = [IsAuthenticated]
      
    def get(self,request,pk):
        try:
            cesspool_request = CesspoolRequest.objects.get(user=request.user,id=pk)
            serializer = CesspoolRequestSerializer(cesspool_request)
            data = serializer.data
            cesspool_images = CesspoolRequest_images.objects.filter(Cesspool_id=cesspool_request.id)
            data['cesspool_images']=[img.image.url for img in cesspool_images]
            return Response(data, status=status.HTTP_200_OK)
            
        except CesspoolRequest.DoesNotExist:
            return Response({"message": "No record found"}, status=status.HTTP_200_OK)
            

        
class AdminCesspoolrequestsView(APIView):
    
    permission_classes=[IsAdminUser]
    
    def get(self,request):
        try: 
            cesspoolrequests = CesspoolRequest.objects.all()
            serializer = CesspoolRequestSerializer(cesspoolrequests,many=True)
            data = serializer.data
            for cesspoolrequest in data:
                cesspool_images = CesspoolRequest_images.objects.filter(Cesspool_id=cesspoolrequest['id'])
                cesspoolrequest['cesspool_images']=[img.image.url for img in cesspool_images]
            return Response(data, status=status.HTTP_200_OK)
        
        except CesspoolRequest.DoesNotExist:
         return Response({"message": "No record found"}, status=status.HTTP_200_OK)
     
     
class AdminEachCesspoolrequestview(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self,request,pk):
        
        try: 
            cesspool_request = CesspoolRequest.objects.get(id=pk)
            serializer = CesspoolRequestSerializer(cesspool_request)
            data = serializer.data
            data = serializer.data
            cesspool_images = CesspoolRequest_images.objects.filter(Cesspool_id=cesspool_request.id)
            data['cesspool_images']=[img.image.url for img in cesspool_images]
            return Response(data, status=status.HTTP_200_OK)

        except CesspoolRequest.DoesNotExist:
            return Response({"message": "No record found"}, status=status.HTTP_200_OK)
        
        
class AdminUpdateCesspoolRequestStatus(APIView):
    permission_classes = [IsAdminUser]
    
    def put(self,request,pk):
        
        cesspoolrequest = get_object_or_404(CesspoolRequest, pk=pk)
        serializer = CessPoolStatusUpdateSerializer(cesspoolrequest, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Status updated successfully."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class BannersView(APIView):
    permission_classes=[]
    def get(self,request):
        try:
          banners = PromotionalBanners.objects.all()
          serializer = BannerSerializer(banners,many=True)
          return Response(serializer.data,status=status.HTTP_200_OK)  

        except PromotionalBanners.DoesNotExist:
          return Response({"message":"no banners found"},status=status.HTTP_200_OK)  
      
class CreateBannerView(APIView):
    permission_classes=[IsAdminUser]
    def post(self,request):
        serializer = BannerSerializer(data=request.data)   
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"banner created successfully"},status=status.HTTP_200_OK) 
        

class DeleteBannerView(APIView):
    permission_classes=[IsAdminUser]
    def delete(self,request,pk):
        try:
            banner = PromotionalBanners.objects.get(id=pk)
            banner.delete()
            return Response({"message":"banner deleted successfully"}, status=status.HTTP_200_OK)
        except PromotionalBanners.DoesNotExist:
            return Response({"message":"Banner not found"}, status=status.HTTP_404_NOT_FOUND)

 
class UpdateBannerView(APIView):
    permission_classes=[IsAdminUser]
    def put(self,request,pk):
        
        banner = get_object_or_404(PromotionalBanners,id=pk)
        serializer = BannerSerializer(banner,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Banner updated successfully"},status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UserNotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)   
    

class FilterNotifications(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        user=request.user  
        category = request.query_params.get('category')
        if not category :
            return Response(
                {"error": "Missing category type in query parameters."},
                status=status.HTTP_400_BAD_REQUEST
            )
        notifications = Notification.objects.filter(user=user,category=category).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)   



class NotificationDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        user=request.user  
        booking_id = request.query_params.get('booking_id')
        service_type = request.query_params.get('service_type')
        
        if not service_type or not booking_id:
            return Response(
                {"error": "Missing service_type or booking_id in query parameters."},
                status=status.HTTP_400_BAD_REQUEST
            )

        service_type = service_type.lower()

        if service_type == "waste pickup":
            booking = get_object_or_404(Requests, booking_id=booking_id, service_type=service_type,user=user)
            serializer = RequestSerializer(booking)

        elif service_type == "mandap booking":
            booking = get_object_or_404(
                Kalyanmandap_booking.objects.select_related('kalyanmandap'),
                booking_id=booking_id,
                service_type=service_type,user=user
            )
            serializer = KalyanmandapBookingSerializer(booking)
            
        elif service_type == "cesspool":
            booking = get_object_or_404(CesspoolRequest, booking_id=booking_id, service_type=service_type,user=user)
            serializer = CesspoolRequestSerializer(booking)  
            
        elif service_type == "complaints":
            booking = get_object_or_404(Complaint, booking_id=booking_id, service_type=service_type,user=user)
            serializer = ComplaintSerializer(booking)            

        else:
            return Response(
                {"error": f"Invalid service_type: {service_type}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class Updatepaymentview(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request):
        user=request.user  
        booking_id = request.query_params.get('booking_id')
        service_type = request.query_params.get('service_type')
        
        if not service_type or not booking_id:
            return Response(
                {"error": "Missing service_type or booking_id in query parameters."},
                status=status.HTTP_400_BAD_REQUEST
            )

        service_type = service_type.lower()

        if service_type == "waste pickup":
            booking = get_object_or_404(Requests, booking_id=booking_id, service_type=service_type, user=user)
            booking.payment_status = "Completed"  
            booking.save()
        elif service_type == "mandap booking":
            booking = get_object_or_404(
                Kalyanmandap_booking.objects.select_related('kalyanmandap'),
                booking_id=booking_id, service_type=service_type, user=user
            )
            booking.payment_status = "Completed"  
            booking.save()
            
        elif service_type == "cesspool":
            booking = get_object_or_404(CesspoolRequest, booking_id=booking_id, service_type=service_type, user=user)
            booking.payment_status = "Completed"  
            booking.save()
        
        else:
            return Response(
                {"error": f"Invalid service_type: {service_type}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"message": "Payment status updated successfully."}, status=status.HTTP_200_OK)
        
        
    
    
    

        
                             
        
        
          
        

              
        
              

                
     
        
           
            
    
    
    
                    
            
        
        
        
     
       
    
    
        
