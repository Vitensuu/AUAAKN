from django.contrib import admin
from .models import Post, ContactInformation, PostAttachment, Rating, Favorite, City
from django.core.exceptions import ValidationError
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
# --- Inline classes ---
class ContactInformationInline(admin.StackedInline):
    model = ContactInformation
    extra = 0
    can_delete = False

class PostAttachmentInline(admin.TabularInline):
    model = PostAttachment
    extra = 1

class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0
    readonly_fields = ('created_at',)
    can_delete = False

class FavoriteInline(admin.TabularInline):
    model = Favorite
    extra = 0
    readonly_fields = ('created_at',)
    can_delete = False

# --- Admin for Post ---
@admin.register(Post)
class CustomPostAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'edited', 'price_per_day')  # Добавил price_per_day в readonly
    inlines = [ContactInformationInline, PostAttachmentInline, RatingInline, FavoriteInline]

    fieldsets = (
        ('Author', {"fields": ('author',)}),
        ('Post Information', {"fields": ('title', 'description',)}),
        ('Price & Status', {"fields": ('price_per_month', 'price_per_day', 'is_active')}),
        ('Address', {"fields": ('city', 'street_or_district', 'house_number', 'apartment_number', 'intercom_code')}),
        ('Layout', {"fields": ('rooms', 'floor', 'total_floors')}),
        ('Areas (m²)', {"fields": ('area_total', 'area_living', 'area_kitchen')}),
        ('Coordinates', {"fields": ('latitude', 'longitude')}),
        ('Additional information', {"fields": ('created_at', 'edited',)}),
    )

    add_fieldsets = (
        ('Author', {"fields": ('author',)}),
        ('Post Information', {"fields": ('title', 'description',)}),
        ('Price & Status', {"fields": ('price_per_month', 'is_active')}),
        ('Address', {"fields": ('city', 'street_or_district', 'house_number', 'apartment_number', 'intercom_code')}),
        ('Layout', {"fields": ('rooms', 'floor', 'total_floors')}),
        ('Areas (m²)', {"fields": ('area_total', 'area_living', 'area_kitchen')}),
        ('Coordinates', {"fields": ('latitude', 'longitude')}),
    )

    list_display = ('author', 'title', 'price_per_month', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'author__username')
    ordering = ('-created_at', )
    list_filter = ('is_active', 'author', 'city', 'rooms')

    def get_fieldsets(self, request, obj=None):
        return self.fieldsets if obj else self.add_fieldsets


# --- Admin for ContactInformation ---
@admin.register(ContactInformation)
class ContactInformationAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Contact information for post', {"fields": ('phone_number', 'email', 'adress')}),
        ('Post', {"fields": ('post',)}),
    )
    list_display = ('phone_number', 'email', 'adress', 'post')
    readonly_fields = ('adress',)
    search_fields = ('post__title',)
    ordering = ('post',)
    list_filter = ('post',)

    def save_model(self, request, obj, form, change):
        if not obj.phone_number and not obj.email:
            raise ValidationError("You must provide either a phone number or an email.")
        super().save_model(request, obj, form, change)

# --- Admin for PostAttachment ---
@admin.register(PostAttachment)
class CustomPostAttachmentAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Files for posts', {"fields": ('name', 'file',)}),
        ('Post', {"fields": ('post',)}),
    )
    list_display = ('name', 'file', 'post')
    search_fields = ('post__title',)
    ordering = ('post',)
    list_filter = ('post',)

    def get_fieldsets(self, request, obj=None):
        return self.fieldsets if obj else (
            ('Files for posts', {"fields": ('file',)}),
            ('Post', {"fields": ('post',)}),
        )

    def save_model(self, request, obj, form, change):
        if not obj.name:
            obj.name = obj.file.name.split('.')[0].capitalize()
        super().save_model(request, obj, form, change)

# --- Admin for Rating ---
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'score', 'created_at')
    search_fields = ('post__title', 'user__username')
    list_filter = ('score', 'created_at', 'post')
    ordering = ('-created_at',)

# --- Admin for Favorite ---
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    search_fields = ('post__title', 'user__username')
    list_filter = ('created_at', 'post')
    ordering = ('-created_at',)
