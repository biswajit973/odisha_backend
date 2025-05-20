from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email,password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    dob = models.DateField(null=True, blank=True)  
    address = models.TextField(blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Requests(models.Model):
    
   
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='requests',default=0)
    type = models.CharField(max_length=100)
    description = models.TextField()
    waste_type = models.CharField(max_length=200,null=True)
    waste_type_other = models.TextField()
    location=models.CharField(max_length=100)
    address=models.TextField(blank=True,null=True)
    date=models.DateField(blank=True,null=True)
    house_number=models.CharField(max_length=100,blank=True,null=True)
    floor=models.CharField(max_length=100,blank=True,null=True) 
    block=models.CharField(max_length=100,blank=True,null=True)
    landmark=models.CharField(max_length=100,blank=True,null=True)
    contact_number=models.CharField(max_length=100)
    time_slot=models.CharField(max_length=100)
    payment_method=models.CharField(max_length=100)
    payment_status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    
    


class Request_images(models.Model):
    request = models.ForeignKey(Requests, on_delete=models.CASCADE, related_name='request_images')
    image = models.ImageField(upload_to='request_images/')
    
    
class StatusUpdates(models.Model):
    request = models.ForeignKey(Requests, on_delete=models.CASCADE, related_name='statusupdates')
    status = models.CharField(max_length=100)
    comment = models.TextField()
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='statusupdates')
    timestamp = models.DateTimeField(auto_now_add=True)
    



class Kalyanmandap(models.Model):
    mandap_name = models.CharField(max_length=100)
    mandap_description = models.TextField(blank=True,null=True)
    mandap_address = models.TextField(blank=True,null=True)
    mandap_contact_number = models.CharField(max_length=100,blank=True,null=True)    
    mandap_capacity = models.IntegerField(blank=True,null=True)
    mandap_amenities = models.TextField(blank=True,null=True)
    mandap_minimum_booking_unit = models.CharField (max_length=100,blank=True,null=True)
    mandap_price_range = models.CharField(max_length=100,blank=True,null=True)
    mandap_price_note = models.TextField(blank=True,null=True)
    active = models.BooleanField(default=True)

class Kalyanmandap_images(models.Model):
    Kalyanmandap = models.ForeignKey(Kalyanmandap, on_delete=models.CASCADE, related_name='kalyanmandap_images')
    image = models.ImageField(upload_to='kalyanmandap_images/')    
    
class Kalyanmandap_booking(models.Model):
    kalyanmandap = models.ForeignKey(Kalyanmandap, on_delete=models.CASCADE, related_name='kalyanmandap_booking')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kalyanmandap_booking')
    occasion = models.CharField(max_length=100)
    number_of_people = models.IntegerField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    duration = models.CharField(max_length=100)
    additional_requests = models.TextField()
    payment_method = models.CharField(max_length=100)
    status= models.CharField(max_length=100,default="pending")
    
       

