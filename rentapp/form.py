from django import forms
from .models import Post, Rating, ContactInformation, Favorite, PostAttachment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 'description', 'is_active', 'price_per_month',
            'city', 'street_or_district', 'house_number', 'apartment_number', 'intercom_code',
            'rooms', 'floor', 'total_floors',
            'area_total', 'area_living', 'area_kitchen',
            'latitude', 'longitude',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Описание'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'price_per_month': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'street_or_district': forms.TextInput(attrs={'class': 'form-control'}),
            'house_number': forms.TextInput(attrs={'class': 'form-control'}),
            'apartment_number': forms.TextInput(attrs={'class': 'form-control'}),
            'intercom_code': forms.TextInput(attrs={'class': 'form-control'}),
            'rooms': forms.Select(attrs={'class': 'form-select'}),
            'floor': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_floors': forms.NumberInput(attrs={'class': 'form-control'}),
            'area_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'area_living': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'area_kitchen': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
        }
        labels = {
            'title': 'Заголовок',
            'description': 'Описание',
            'is_active': 'Активно',
            'price_per_month': 'Цена в месяц',
            'city': 'Город',
            'street_or_district': 'Улица или микрорайон',
            'house_number': 'Номер дома',
            'apartment_number': 'Квартира',
            'intercom_code': 'Домофон',
            'rooms': 'Количество комнат',
            'floor': 'Этаж',
            'total_floors': 'Этажей в доме',
            'area_total': 'Общая площадь (м²)',
            'area_living': 'Жилая площадь (м²)',
            'area_kitchen': 'Площадь кухни (м²)',
            'latitude': 'Широта',
            'longitude': 'Долгота',
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': forms.Select(attrs={'class': 'form-select'}),
        }


class ContactInformationForm(forms.ModelForm):
    class Meta:
        model = ContactInformation
        fields = ['phone_number', 'email', 'adress']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'adress': forms.TextInput(attrs={'class': 'form-control'}),
        }


class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = []  # No fields, just use this to trigger creation (user and post should be set in the view)


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        default_attrs = {'multiple': True, 'class': 'form-control'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput())
        kwargs.setdefault('required', False)
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if not data:
            return []
        if not isinstance(data, (list, tuple)):
            data = [data]

        cleaned_files = []
        errors = []
        for file in data:
            try:
                cleaned_files.append(super().clean(file, initial))
            except forms.ValidationError as e:
                errors.extend(e.error_list)

        if errors:
            raise forms.ValidationError(errors)

        return cleaned_files

from django import forms

class PostAttachmentMultiUploadForm(forms.Form):
    images = MultipleFileField()

class BookingForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

