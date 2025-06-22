from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import Post, Favorite, Rating, Booking, ContactInformation, PostAttachment, City
from .form import (
    PostForm,
    ContactInformationForm,
    PostAttachmentMultiUploadForm,
    RatingForm,
    BookingForm,
)
from django.views.decorators.http import require_POST


def main_page(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'post/main_page.html', {'posts': posts})


def post_list(request):
    posts = Post.objects.filter(is_active=True).order_by('-created_at')
    cities = City.objects.all()

    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        posts = posts.filter(price_per_month__gte=price_min)
    if price_max:
        posts = posts.filter(price_per_month__lte=price_max)

    rooms = request.GET.get('rooms')
    if rooms:
        posts = posts.filter(rooms=rooms)

    city = request.GET.get('city')
    if city:
        posts = posts.filter(city__name=city)

    area_min = request.GET.get('area_min')
    area_max = request.GET.get('area_max')
    if area_min:
        posts = posts.filter(area_total__gte=area_min)
    if area_max:
        posts = posts.filter(area_total__lte=area_max)

    has_image = request.GET.get('has_image')
    if has_image:
        posts = posts.annotate(image_count=Count('attachments')).filter(image_count__gt=0)

    for post in posts:
        post.att = PostAttachment.objects.filter(post=post)

    room_choices = range(1, 11)  # список чисел от 1 до 10

    return render(request, 'post/post_list.html', {
        'posts': posts,
        'cities': cities,
        'room_choices': room_choices,
    })

@login_required
def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        contact_form = ContactInformationForm(request.POST)
        image_form = PostAttachmentMultiUploadForm(request.POST, request.FILES)

        if post_form.is_valid() and contact_form.is_valid() and image_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()

            contact_info = contact_form.save(commit=False)
            contact_info.post = post
            contact_info.save()

            for file in image_form.cleaned_data['images']:
                PostAttachment.objects.create(post=post, file=file)

            messages.success(request, 'Объявление успешно создано!')
            return redirect('post_detail', post_id=post.id)
    else:
        post_form = PostForm()
        contact_form = ContactInformationForm()
        image_form = PostAttachmentMultiUploadForm()

    return render(request, 'post/create_post.html', {
        'post_form': post_form,
        'contact_form': contact_form,
        'image_form': image_form,
    })


@login_required
def edit_post(request, pid):
    post = get_object_or_404(Post, pk=pid)
    post_attachments = PostAttachment.objects.filter(post=post)

    try:
        contact_info = ContactInformation.objects.get(post=post)
    except ContactInformation.DoesNotExist:
        contact_info = None

    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        contact_form = ContactInformationForm(request.POST, instance=contact_info)
        image_form = PostAttachmentMultiUploadForm(request.POST, request.FILES)

        if post_form.is_valid() and contact_form.is_valid() and image_form.is_valid():
            post = post_form.save(commit=False)
            post.edited = True
            post.save()

            contact_info = contact_form.save(commit=False)
            contact_info.post = post
            contact_info.save()

            for file in image_form.cleaned_data['images']:
                PostAttachment.objects.create(post=post, file=file)

            chosen = request.POST.getlist('attachments')
            for image_id in chosen:
                try:
                    PostAttachment.objects.get(pk=int(image_id), post=post).delete()
                except PostAttachment.DoesNotExist:
                    pass

            messages.success(request, 'Объявление успешно обновлено!')
            return redirect('post_detail', post_id=post.pk)
    else:
        post_form = PostForm(instance=post)
        contact_form = ContactInformationForm(instance=contact_info)
        image_form = PostAttachmentMultiUploadForm()

    return render(request, 'post/post_edit.html', {
        'post_form': post_form,
        'contact_form': contact_form,
        'image_form': image_form,
        'post_att': post_attachments,
        'post': post,
    })

@login_required
def post_delete(request, pid):
    post = get_object_or_404(Post, pk=pid)
    post.delete()
    return redirect('post_list')

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    rating_form = RatingForm()
    is_favorite = False

    # Получаем контактную информацию, если есть
    contact_info = ContactInformation.objects.filter(post=post).first()

    # Получаем все вложения
    attachments = PostAttachment.objects.filter(post=post)

    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(post=post, user=request.user).exists()

    return render(request, 'post/post_detail.html', {
        'post': post,
        'rating_form': rating_form,
        'is_favorite': is_favorite,
        'contact_info': contact_info,
        'attachments': attachments,
    })



@login_required
@require_POST
def add_rating(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = RatingForm(request.POST)

    if form.is_valid():
        Rating.objects.update_or_create(
            post=post,
            user=request.user,
            defaults={'score': form.cleaned_data['score']}
        )
        messages.success(request, 'Your rating has been saved.')

    return redirect('post_detail', post_id=post.id)


@login_required
@require_POST
def toggle_favorite(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    favorite, created = Favorite.objects.get_or_create(post=post, user=request.user)

    if not created:
        favorite.delete()
        messages.info(request, 'Removed from favorites.')
    else:
        messages.success(request, 'Added to favorites.')

    return redirect('post_detail', post_id=post.id)


@login_required
def book_property(request, post_id):
    property_post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            num_days = (end_date - start_date).days
            total_price = num_days * property_post.price_per_day

            Booking.objects.create(
                user=request.user,
                property_post=property_post,
                start_date=start_date,
                end_date=end_date,
                total_price=total_price
            )

            return redirect('booking_success')
    else:
        form = BookingForm()

    return render(request, 'rentapp/book_property.html', {
        'form': form,
        'property': property_post
    })
from django.shortcuts import render
from .models import Post

def search_posts(request):
    query = request.GET.get('q', '')  
    results = Post.objects.filter(title__icontains=query) if query else []
    return render(request, 'rentapp/search_results.html', {'results': results, 'query': query})
