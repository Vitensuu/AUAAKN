from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from .models import Notification
from django.contrib.auth import get_user_model
User = get_user_model()

@login_required
def notification_list(request):
    notifications = request.user.notifications.order_by('-created_at')
    return render(request, 'dashboard/notification_list.html', {'notifications': notifications})

@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'ok', 'message': 'Notification marked as read'})

@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.delete()
    return JsonResponse({'status': 'ok', 'message': 'Notification deleted'})

