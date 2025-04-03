from django.db import models
from django.contrib.auth.models import User  # Используем встроенную модель пользователей

class Category(models.TextChoices):
    APARTMENTS = "Apartments", "Apartments"
    HOUSES = "Houses", "Houses"
    ROOMS = "Rooms", "Rooms"
    COWORKING = "Co-working", "Co-working"
    VILLAS = "Villas", "Villas"
    STUDIOS = "Studios", "Studios"

class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.APARTMENTS
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена с двумя знаками после запятой
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Связь с пользователем
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.price}$ by {self.author.username} : {self.created_at}"

class ApartmentPost(Post):
    class Meta:
        proxy = True  

    objects = models.Manager()

    @classmethod
    def get_apartments(cls):
        return cls.objects.filter(category=Category.APARTMENTS)

