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
    role = models.CharField(max_length=100,blank=True,null=True)
    department = models.CharField(max_length=100,blank=True,null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


    
    
    
STATUS_CHOICES = [
        ('pending', 'pending'),
        ('approved', 'approved'),
        ('scheduled', 'scheduled'),
        ('rejected', 'rejected'),
        ('completed','completed')
    ]    

from django.db import models, transaction

class BookingSequence(models.Model):
    
    last_booking_id = models.BigIntegerField(default=1000)

    @classmethod
    def get_next_booking_id(cls):
        with transaction.atomic():
            seq, created = cls.objects.get_or_create(pk=1)
            seq.last_booking_id += 1
            seq.save()
            return seq.last_booking_id
        

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    booking_id = models.BigIntegerField(null=True,blank=True)
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=50,null=True,blank=True)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} for booking {self.booking_id}"
    
    

        
        
class Requests(models.Model):
    
    booking_id = models.BigIntegerField(unique=True, editable=False,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='requests',default=0)
    service_type = models.CharField(default="waste pickup",max_length=100)
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
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    comment = models.TextField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        is_update = self.pk is not None
        old_status = None
        old_comment = None

        if is_update:
            old = Requests.objects.get(pk=self.pk)
            old_status = old.status
            old_comment = old.comment

        if not self.booking_id:
            self.booking_id = BookingSequence.get_next_booking_id()

        super().save(*args, **kwargs)

        if is_update and (self.status != old_status or self.comment != old_comment):
            Notification.objects.create(
                user=self.user,
                booking_id=self.booking_id,
                title=f"Update on your {self.service_type} request",
                status=self.status,
                comment=self.comment or ''
            )

    


class Request_images(models.Model):
    request = models.ForeignKey(Requests, on_delete=models.CASCADE, related_name='request_images')
    image = models.ImageField(upload_to='request_images/')
    
    

    



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
    booking_id = models.BigIntegerField(unique=True, editable=False,null=True,blank=True)
    kalyanmandap = models.ForeignKey(Kalyanmandap, on_delete=models.CASCADE, related_name='kalyanmandap_booking')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kalyanmandap_booking')
    service_type = models.CharField(default="mandap booking",max_length=100)
    occasion = models.CharField(max_length=100)
    number_of_people = models.IntegerField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    duration = models.CharField(max_length=100)
    additional_requests = models.TextField()
    payment_method = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    comment = models.TextField(null=True,blank=True)
    
    def save(self, *args, **kwargs):
        is_update = self.pk is not None
        old_status = None
        old_comment = None

        if is_update:
            old = Kalyanmandap_booking.objects.get(pk=self.pk)
            old_status = old.status
            old_comment = old.comment

        if not self.booking_id:
            self.booking_id = BookingSequence.get_next_booking_id()

        super().save(*args, **kwargs)

        if is_update and (self.status != old_status or self.comment != old_comment):
            Notification.objects.create(
                user=self.user,
                booking_id=self.booking_id,
                title=f"Update on your {self.service_type} request",
                status=self.status,
                comment=self.comment or ''
            )
    
    
 
   
    

    
class ComplaintCategory(models.Model):
    name = models.CharField(max_length=255)
    active_status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class ComplaintSubCategory(models.Model):
    category = models.ForeignKey(ComplaintCategory, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_paid_service = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"

    

class Complaint(models.Model):
    booking_id = models.BigIntegerField(unique=True, editable=False,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ComplaintCategory, on_delete=models.CASCADE, null=True)
    subcategory = models.ForeignKey(ComplaintSubCategory, on_delete=models.CASCADE, null=True, blank=True)
    custom_category = models.CharField(max_length=255, blank=True, null=True)  
    service_type = models.CharField(default="complaints",max_length=100)
    location = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    description = models.TextField()
    submitted_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    comment = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        is_update = self.pk is not None
        old_status = None
        old_comment = None

        if is_update:
            old = Complaint.objects.get(pk=self.pk)
            old_status = old.status
            old_comment = old.comment

        if not self.booking_id:
            self.booking_id = BookingSequence.get_next_booking_id()

        super().save(*args, **kwargs)

        if is_update and (self.status != old_status or self.comment != old_comment):
            Notification.objects.create(
                user=self.user,
                booking_id=self.booking_id,
                title=f"Update on your {self.service_type} request",
                status=self.status,
                comment=self.comment or ''
            )

class Complaint_images(models.Model):
    complaint = models.ForeignKey(Complaint, related_name='complaint_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='complaint_images/')   
    
    

class CesspoolRequest(models.Model):
    booking_id = models.BigIntegerField(unique=True, editable=False,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    service_type = models.CharField(default="cesspool",max_length=100)
    contact_number = models.CharField(max_length=15)
    location = models.CharField(max_length=255)  
    address = models.TextField()
    description = models.TextField()
    waste_tank_type = models.CharField(max_length=100)
    capacity = models.CharField(max_length=100,null=True,blank=True)
    urgency_level = models.CharField(max_length=20,null=True,blank=True)
    preferred_datetime = models.DateTimeField(blank=True, null=True) 
    accessibility_note = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        is_update = self.pk is not None
        old_status = None
        old_comment = None

        if is_update:
            old = CesspoolRequest.objects.get(pk=self.pk)
            old_status = old.status
            old_comment = old.comment

        if not self.booking_id:
            self.booking_id = BookingSequence.get_next_booking_id()

        super().save(*args, **kwargs)

        # Notify only if status or comment changed
        if is_update and (self.status != old_status or self.comment != old_comment):
            Notification.objects.create(
                user=self.user,
                booking_id=self.booking_id,
                title=f"Update on your {self.service_type} request",
                status=self.status,
                comment=self.comment or ''
            )
            
            
            
class CesspoolRequest_images(models.Model):
    Cesspool = models.ForeignKey(CesspoolRequest,on_delete=models.CASCADE,related_name='cesspool_images')
    image = models.ImageField(upload_to='cesspool_images/')   
    
 
class PromotionalBanners(models.Model):    
    hyperlink = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True,null=True)
    banner_image = models.ImageField(upload_to="banner_images/")
    


    
    
    
    
    
    
    

        
        

    

    
 
    


    
    

