from django.shortcuts import get_object_or_404, render
import random
from django.shortcuts import render

from myapp.models import *
from .models import *

from .permissions import IsSuperUser

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
import pyotp

from django.contrib.auth import get_user_model


# Create your views here.
User = get_user_model()

class AdminLoginView(APIView):
    permission_classes = []
    serializer_class = AdminLoginSerializer

    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        print("Request data:", request.data) 
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, email=email, password=password)
            if user is not None:
                if not user.is_superuser and not user.is_admin:
                    return Response(
                        {"error": "please login with admin credentials."},
                        status=status.HTTP_403_FORBIDDEN
                    )
                
                if not user.is_staff:
                    user.is_staff = True  
                    user.save()

                refresh = RefreshToken.for_user(user)
                print("Refresh token:", refresh)

                return Response({
                    "success": True,
                    "message": "Login successful",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "email": user.email,
                    'department':user.department,
                    'is_superuser':user.is_superuser,
                }, status=status.HTTP_200_OK)

            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
   



from django.contrib.auth.hashers import make_password

class AdminListAPIView(APIView):
    permission_classes = [IsSuperUser]
    serializer_class = AdminListSerializer
    def get(self, request):
        admins = User.objects.filter(is_admin=True)
        serializer = AdminListSerializer(admins, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class CreateAdminAPIView(APIView):
    permission_classes = [IsSuperUser]
    def post(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('role')
        department = request.data.get('department')

        if not (first_name and last_name and email and password and role and department):
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        new_admin = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=role,
            department=department,
            password=make_password(password),
            is_staff=True,  
            is_admin=True,
            is_superuser=False
        
        )

        return Response({'success': 'Admin created successfully'}, status=status.HTTP_201_CREATED)

class UpdateAdminView(APIView):    
    permission_classes=[IsSuperUser]
    def put(self,request,pk):
        try:
            admin = User.objects.get(id=pk)
        except User.DoesNotExist :
              return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UpdateAdminSerializer(admin,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Details Updated Successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
        
        
        
            
    
class DeleteAdminAPIView(APIView):
    permission_classes = [IsSuperUser]
    serializer_class = AdminListSerializer
    def delete(self, request, pk):
        admin = User.objects.get(pk=pk)
        admin.delete()
        return Response({'success': 'Admin deleted successfully'}, status=status.HTTP_200_OK)
        


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
    

class AdminUpdateRequestStatusView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, booking_id):
        try:
            booking = Requests.objects.get(id=booking_id)
        except Requests.DoesNotExist:
            return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = RequestStatusUpdateSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Request status updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    



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
        
class AdminUpdateComplaintReportStatusView(APIView):
    permission_classes = [IsAdminUser]
    def put(self, request, pk):
        report = get_object_or_404(Complaint, pk=pk)
        serializer = ComplaintReportStatusUpdateSerializer(report, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Status updated successfully."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



        
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


class AdminListAllBookingsView(APIView):
    permission_classes = [IsAdminUser]  

    def get(self, request):
        bookings = Kalyanmandap_booking.objects.all().order_by('-start_datetime')
        serializer = AdminKalyanmandapBookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)              


class AdminUpdateMandapBookingStatusView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, booking_id):
        try:
            booking = Kalyanmandap_booking.objects.get(id=booking_id)
        except Kalyanmandap_booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MandapBookingStatusUpdateSerializer(booking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Booking status updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
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



    