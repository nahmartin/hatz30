from django.contrib import admin
from .models import Car, CarPhoto, CarSold


class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'price', 'year', 'short_info')
    list_filter = ('brand', 'model', 'year')
    search_fields = ('brand', 'model')

    actions = ['delete_selected_cars']

    def delete_selected_cars(self, request, queryset):
        for car in queryset:
            car.delete()

    delete_selected_cars.short_description = "Delete selected cars"


admin.site.register(Car, CarAdmin)


class CarPhotoAdmin(admin.ModelAdmin):
    list_display = ['car', 'display_photos']
    search_fields = ['photo1']

    def display_photos(self, obj):
        return obj.photo1[:50]

    display_photos.short_description = 'Photos'

    def save_model(self, request, obj, form, change):
        # Split the input by lines and create separate instances for each photo link
        photo_links = form.cleaned_data['photo1'].split('\n')
        for link in photo_links:
            if link.strip():  # Ignore empty lines
                link_stripped = link.strip()
                if not CarPhoto.objects.filter(photo1=link_stripped).exists():
                    car_photo = CarPhoto(car=obj.car, photo1=link_stripped)
                    car_photo.save()
                else:
                    self.message_user(request, f'The photo link "{link_stripped}" already exists in the database.',
                                      level='WARNING')

        super().save_model(request, obj, form, change)


admin.site.register(CarPhoto, CarPhotoAdmin)


class CarSoldAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'price', 'year', 'short_info')
    list_filter = ('brand', 'model', 'year')
    search_fields = ('brand', 'model', 'photo_test_main')  # Added 'photo_test_main' to search fields

    actions = ['delete_selected_cars']

    def delete_selected_cars(self, request, queryset):
        for car in queryset:
            car.delete()

    delete_selected_cars.short_description = "Delete selected cars"


admin.site.register(CarSold, CarSoldAdmin)
