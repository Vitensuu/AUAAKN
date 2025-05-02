from django.contrib import admin
from .models import Post, ContactInformation, PostAttachment
from django.core.exceptions import ValidationError

class ContactInformationInline(admin.StackedInline):
    model = ContactInformation
    extra = 0
    can_delete = False

class PostAttachmentInline(admin.TabularInline):
    model = PostAttachment
    extra = 1

@admin.register(ContactInformation)
class ContactInformationAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Contact information for post', {"fields":('phone_number', 'email', 'adress',)}),
        ('Post', {"fields":('post',)}),
    )
    add_fieldsets = (
        ('Contact information for post', {"fields":('phone_number', 'email', 'adress',)}),
        ('Post', {"fields":('post',)}),
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


@admin.register(PostAttachment)
class CustomPostAttachmentAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Files for posts', {"fields": ('name', 'file',)}),
        ('Post', {"fields": ('post',)}),
    )
    add_fieldsets = (
        ('Files for posts', {"fields": ('file',)}),
        ('Post', {"fields": ('post',)}),
    )
    list_display = ('name', 'file', 'post')
    search_fields = ('post__title',)
    ordering = ('post',)
    list_filter = ('post',)

    def get_fieldsets(self, request, obj=None):
        if obj:
            return self.fieldsets
        return self.add_fieldsets

    def save_model(self, request, obj, form, change):
        if not obj.name:
            obj.name = obj.file.name.split('.')[0].capitalize()
        super().save_model(request, obj, form, change)


@admin.register(Post)
class CustomPostAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'edited') 
    inlines = [ContactInformationInline, PostAttachmentInline]  
    fieldsets = (
        ('Author', {"fields": ('author',)}),
        ('Post Information', {"fields": ('title', 'description',)}),
        ('Price', {"fields": ('price',)}),
        ('Additional information', {"fields": ('created_at', 'edited',)}),
    )

    add_fieldsets = (
        ('Author', {"fields": ('author',)}),
        ('Post Information', {"fields": ('title', 'description',)}),
        ('Price', {"fields": ('price',)}),
    )

    list_display = ('author', 'title', 'created_at')
    search_fields = ('title', 'description') 
    ordering = ('-created_at', )

    def get_fieldsets(self, request, obj=None):
        if obj:
            return self.fieldsets
        return self.add_fieldsets

