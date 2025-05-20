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


from django.contrib.auth import get_user_model


# Create your views here.
class RegisterView(APIView):
    permission_classes = []
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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

class AdminLoginView(APIView):
    permission_classes = []
    serializer_class = AdminLoginSerializer

    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, email=email, password=password)
            if user is not None:
                
                if not user.is_staff:
                    user.is_staff = True  
                    user.save()

                refresh = RefreshToken.for_user(user)

                return Response({
                    "message": "Admin Login successful",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "email": user.email
                }, status=status.HTTP_200_OK)

            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminLogoutView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
   
    
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
        
        
class ResetPasswordRequestView(APIView):
    permission_classes = []
    serializer_class = ResetPasswordRequestSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = f"https://mobile.wemakesoftwares.com/reset-password/?uid={uid}&token={token}"
            send_mail(
                'Reset Password Request',
                f'Click the link to reset your password: {reset_url}',
                 from_email="pk93917@gmail.com",
                recipient_list=[email],
                fail_silently=False
            )   
            return Response({'message': 'Reset password email sent'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        
        
class PasswordResetView(APIView):
    permission_classes = []
    serializer_class = PasswordResetSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            uid = serializer.validated_data['uid']
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            
            try:
                uid = urlsafe_base64_decode(uid).decode()
                user = User.objects.get(pk=uid)
            except (User.DoesNotExist, ValueError, TypeError):
                return Response({"detail": "Invalid UID"}, status=status.HTTP_400_BAD_REQUEST)

            if not default_token_generator.check_token(user, token):
                return Response({"detail": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            return Response({"detail": "Password reset successful"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                

class AccountDetails(APIView):    
    permission_classes=[IsAuthenticated]      
    serializer_class = UserProfileSerializer      

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response({"userDetails":serializer.data}, status=status.HTTP_200_OK)
    

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
        
        return Response({"message": "Request created successfully"}, status=status.HTTP_201_CREATED)
        
        
        
        
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
    

class EachUserRequestView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class   = EachRequestSerializer
    
    def get(self, request, pk):
        
        requests = Requests.objects.filter(user_id=pk)
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
        count = Requests.objects.filter(type='Personal Waste').count()
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
        requests = Requests.objects.filter(type='Personal Waste')
        if not requests.exists():
            return Response({"message": "No requests found."}, status=status.HTTP_200_OK)
        
        serializer = self.serializer_class(requests, many=True)
        data = serializer.data

        for request in data:
            request_images = Request_images.objects.filter(request_id=request['id'])
            request['request_images'] = [img.image.url for img in request_images]

        return Response(data, status=status.HTTP_200_OK)    
        
       

class StatusUpdateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request,pk):
        serializer = StatusUpdateSerializer(data=request.data)
        if serializer.is_valid():
            try:
               request_instance =  Requests.objects.get(id=pk)
            except Requests.DoesNotExist:
                return Response({"error": "Request not found."}, status=status.HTTP_404_NOT_FOUND)
            
            if StatusUpdates.objects.filter(request=request_instance).exists():
                return Response({"error": "Status has already been updated for this request."}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save(request=request_instance,updated_by=request.user)
            return Response({"message": "Status updated successfully."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    
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
        bookings = Kalyanmandap_booking.objects.filter(user=request.user).order_by('-start_datetime')
        serializer = KalyanmandapBookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
class AdminListAllBookingsView(APIView):
    permission_classes = [IsAdminUser]  

    def get(self, request):
        bookings = Kalyanmandap_booking.objects.all().order_by('-start_datetime')
        serializer = AdminKalyanmandapBookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    
    


class AdminUpdateBookingStatusView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, booking_id):
        try:
            booking = Kalyanmandap_booking.objects.get(id=booking_id)
        except Kalyanmandap_booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookingStatusUpdateSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Booking status updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    