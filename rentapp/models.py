from django.db import models
import os
from django.core.exceptions import ValidationError
from user.models import User

class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.price} KZT by {self.author.username} : {self.created_at}"

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
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Post')
    
    def save(self, *args, **kwargs):
        file_name = os.path.splitext(self.file.name)[0].replace('_', ' ').capitalize()
        self.name = (file_name[:50] + '...') if len(file_name) > 50 else file_name
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

<<<<<<< Updated upstream
    objects = models.Manager()

    @classmethod
    def get_apartments(cls):
        return cls.objects.filter(category=Category.APARTMENTS)
=======
    def __str__(self):
        return f'Image "{self.name}" for post "{self.post.title}"'

>>>>>>> Stashed changes
