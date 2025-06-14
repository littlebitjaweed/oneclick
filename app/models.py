from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

# Create your models here.
class Event(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('adventure', 'Adventure'),
        ('sports', 'Sports'),
        ('diy', 'DIY'),
        ('crafts', 'Crafts'),
        ('Entertainment', 'Entertainment'),
        ('Kids', 'Kids'),
        ('Cooking', 'Cooking'),
        ('other', 'Other')
    ]

    CITY_CHOICES = [
        ('Bengaluru', 'Bengaluru'),
        ('Delhi', 'Delhi'),
        ('Hyderabad', 'Hyderabad'),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    city = models.CharField(max_length=20, choices=CITY_CHOICES, default='Bengaluru')
    image = models.ImageField(upload_to='event_images/', default="event_images/default.jpg")
    
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    convenience_fee = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    gst_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=18.00)

    highlight_image1 = models.ImageField(upload_to='event_highlights/', blank=True, null=True)
    highlight_image2 = models.ImageField(upload_to='event_highlights/', blank=True, null=True)
    highlight_image3 = models.ImageField(upload_to='event_highlights/', blank=True, null=True)

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('event_detail', kwargs={'pk': self.pk})

    def calculate_total_price(self, participants):
        subtotal = self.price * participants
        gst_amount = (subtotal + self.convenience_fee) * (self.gst_percentage / 100)
        return subtotal + self.convenience_fee + gst_amount


class AvailableDate(models.Model):
    event = models.ForeignKey(Event, related_name='available_dates', on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return self.date.strftime('%B %d, %Y')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default="profile_pictures/default.jpg")
    phone_no = models.CharField(max_length=10)
    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class SellerApplication(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=100)
    tax_id = models.CharField(max_length=100)
    address = models.TextField()
    contact_number = models.CharField(max_length=20)
    documents = models.FileField(upload_to='seller_documents/')
    is_approved = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(SellerApplication, self).save(*args, **kwargs)
        if self.is_approved:
            profile, created = Profile.objects.get_or_create(user=self.user)
            profile.is_seller = True
            profile.save()

    def __str__(self):
        return self.business_name


class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    selected_date = models.ForeignKey(AvailableDate, on_delete=models.CASCADE)
    participants = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.event.name} - {self.selected_date}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participants = models.PositiveIntegerField()
    selected_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.event.name}"


class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return datetime.now() < self.created_at + timedelta(minutes=5)

    def __str__(self):
        return f"{self.user.username} - {self.otp_code}"
