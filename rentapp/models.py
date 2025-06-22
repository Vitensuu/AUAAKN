from django.db import models
import os
from django.core.exceptions import ValidationError
from user.models import User
from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()

class City(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Город")

    def __str__(self):
        return self.name


class Post(models.Model):
    ROOM_CHOICES = [(i, str(i)) for i in range(1, 11)]

    is_active = models.BooleanField(default=True, verbose_name="Активно")
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False, verbose_name="Отредактировано")

    price_per_month = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена в месяц")

    @property
    def price_per_day(self):
        return round(self.price_per_month / Decimal('30.0'), 2)


    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, verbose_name="Город")
    street_or_district = models.CharField(max_length=255, verbose_name="Улица или микрорайон")
    house_number = models.CharField(max_length=10, verbose_name="Номер дома")
    apartment_number = models.CharField(max_length=10, blank=True, null=True, verbose_name="Квартира")
    intercom_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="Домофон")

    rooms = models.PositiveSmallIntegerField(choices=ROOM_CHOICES, verbose_name="Количество комнат")
    floor = models.PositiveSmallIntegerField(verbose_name="Этаж")
    total_floors = models.PositiveSmallIntegerField(verbose_name="Этажей в доме")

    area_total = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Общая площадь (м²)")
    area_living = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Жилая площадь (м²)")
    area_kitchen = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Площадь кухни (м²)")

    
    latitude = models.FloatField(null=True, blank=True, verbose_name="Широта")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Долгота")

    def __str__(self):
        return f"{self.title} - {self.price_per_month} KZT by {self.author.username}"

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(r.score for r in ratings) / ratings.count(), 1)
        return "No ratings"

class Rating(models.Model):
    RATING_CHOICES = [(i, f"{i} ⭐") for i in range(1, 11)]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    score = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user') 

    def __str__(self):
        return f"{self.user.username} rated {self.post.title} - {self.score} ⭐"

class ContactInformation(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="contact_information")
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    adress = models.CharField(max_length=500, blank=True, null=True)

    def clean(self):
        if not self.phone_number and not self.email:
            raise ValidationError("At least one contact method (phone or email) must be provided.")

    def __str__(self):
        return f"Phone: {self.phone_number}, Email: {self.email}"
    

class Favorite(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Favorite by {self.user.username} on {self.post.title}"


def validate_image(file):
    valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
    ext = file.name.split('.')[-1].lower()
    if ext not in valid_extensions:
        raise ValidationError('This is image file!!!Format: jpg, jpeg, png, gif.')

class PostAttachment(models.Model):
    name = models.CharField(verbose_name='Image files name', blank=True, null=True)
    file = models.FileField(upload_to='images/', verbose_name='Image', validators=[validate_image])
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='attachments', verbose_name='Post')  # ✅ added related_name

    def save(self, *args, **kwargs):
        file_name = os.path.splitext(self.file.name)[0].replace('_', ' ').capitalize()
        self.name = (file_name[:50] + '...') if len(file_name) > 50 else file_name
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return f'Image "{self.name}" for post "{self.post.title}"'

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        num_days = (self.end_date - self.start_date).days
        if num_days < 1:
            num_days = 1  
        self.total_price = num_days * self.property_post.price_per_day
        super().save(*args, **kwargs)