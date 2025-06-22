from django.db import models
from user.models import User
from rentapp.models import Post
class RentalRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принято'),
        ('declined', 'Отклонено'),
        ('cancelled', 'Отменено'),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='rental_requests')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rental_requests')
    message = models.TextField(blank=True, null=True)  # сообщение арендодателю
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    decline_reason = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.tenant.username} requests {self.post.title} - {self.status}"

class RentalHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rental_history')
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} rented {self.post.title} from {self.start_date}"

class PaymentHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_history')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=[('topup', 'Пополнение'), ('withdraw', 'Вывод')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} {self.amount} ₽"
