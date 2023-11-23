from uuid import uuid4

from django.contrib import admin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from static.theme_material_kit.utils import send_email
from .models import Car
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


# Create your views here.
@csrf_exempt
def submit_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        last = request.POST.get('last')
        phone = request.POST.get('phone')
        print(f'Name: {name}, Phone: {phone}, last name: {last}')
        subject = 'New Client'
        message = f'Name: {name}\nPhone: {phone}\nLast name: {last}'
        from_email = 'sales@masterpiecevintage.com'  # Use your Titan Mail email address
        recipient_list = 'sales@masterpiecevintage.com'  # Replace with the recipient's email address

        # Call the send_email function to send the email
        send_email(from_email, 'numberone123123ana.', recipient_list, subject, message)

        # Process or store the data as needed.

        # Return a JSON response with a success message.
        return redirect('index')  # 'main' should be the name of the URL pattern for your main page

    # Return a JSON response for invalid requests.
    return JsonResponse({'message': 'Invalid request'})


@csrf_exempt
def submit_contact_modal_form(request):
    if request.method == 'POST':
        name = request.POST.get('contact[name]')
        last = request.POST.get('contact[last_name]')
        phone = request.POST.get('contact[phone]')
        email = request.POST.get('contact[email]')
        country = request.POST.get('contact[country]')
        time_to_call = request.POST.get('contact[time_to_call]')
        comment = request.POST.get('contact[comment]')
        car_link = request.POST.get('contact[car_link]')  # Retrieve the car link
        subject = 'car client'
        message = f'Name: {name}, Last Name: {last}, Phone: {phone}, Email: {email}, Country: {country}, Time to Call: {time_to_call}, Comment: {comment}, Car Link: {car_link}'
        from_email = 'sales@masterpiecevintage.com'  # Use your Titan Mail email address
        recipient_list = 'sales@masterpiecevintage.com'  # Replace with the recipient's email address
        # Process or store the form data as needed.

        print(
            f'Name: {name}, Last Name: {last}, Phone: {phone}, Email: {email}, Country: {country}, Time to Call: {time_to_call}, Comment: {comment}, Car Link: {car_link}')

        send_email(from_email, 'numberone123123ana.', recipient_list, subject, message)
        # You can include additional logic to handle the form data, such as sending emails or storing in a database.

        # Return a JSON response with a success message.
        return redirect('index')

    # Return a JSON response for invalid requests.
    return JsonResponse({'message': 'Invalid request'})


def submit_carfinder_modal_form(request):
    if request.method == 'POST':
        name = request.POST.get('carfinder[name]')
        email = request.POST.get('carfinder[email]')
        message = request.POST.get('carfinder[message]')
        subject = 'Car Finder Inquiry'
        from_email = 'sales@masterpiecevintage.com'  # Use your Titan Mail email address
        recipient_list = 'sales@masterpiecevintage.com'  # Replace with the recipient's email address
        # Process or store the form data as needed.

        print(f'Name: {name}, Email: {email}, Message: {message}')

        send_email(from_email, 'numberone123123ana.', recipient_list, subject, message)
        # You can include additional logic to handle the form data, such as sending emails or storing in a database.

        # Return a JSON response with a success message.
        return JsonResponse({'message': 'Form submitted successfully'})

    # Return a JSON response for invalid requests.
    return JsonResponse({'message': 'Invalid request'})


def index(request):
    cars = Car.objects.all()
    cars_by_brand = {}  # Your existing logic for grouping by brand

    # Extract parameters from the query string
    price_gteq = request.GET.get('q[price_gteq]')
    price_lteq = request.GET.get('q[price_lteq]')
    make_eq = request.GET.get('q[make_eq]')
    search_cont = request.GET.get('q[ftx_search_cont]')
    year_filter = request.GET.get('q[year_eq]')

    # Apply filters based on the extracted parameters
    if price_gteq and price_lteq:
        cars = cars.filter(price__gte=price_gteq, price__lte=price_lteq)

    if make_eq:
        cars = cars.filter(brand=make_eq)

    if search_cont:
        # Adjust this based on your model fields for searching
        cars = cars.filter(Q(brand__icontains=search_cont) | Q(model__icontains=search_cont))

    if year_filter:
        # Adjust this based on your model field for the year
        cars = cars.filter(year=year_filter)

    # Your existing logic for grouping by brand
    for car in cars:
        brand = car.brand
        if brand not in cars_by_brand:
            cars_by_brand[brand] = []
        cars_by_brand[brand].append(car)

    brands = list(cars_by_brand.keys())

    # Your existing logic for rendering the template
    return render(request, 'pages/index.html', {'brands': brands, 'cars_by_brand': cars_by_brand, 'car_list': cars})


def feedbackurl(request):
    cars = Car.objects.all()

    # Create a dictionary to store cars grouped by brand
    cars_by_brand = {}
    cars_by_type = {}

    for car in cars:
        brand = car.brand

        if brand not in cars_by_brand:
            cars_by_brand[brand] = []
        cars_by_brand[brand].append(car)

    # Get a list of all unique brand names
    brands = list(cars_by_brand.keys())

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Process or store the data as needed.
        # In this example, we'll just send an email with the submitted data.
        subject = 'Feedback from Website'
        email_message = f'Name: {name}\nPhone: {phone}\nMessage: {message}'
        from_email = 'sales@masterpiecevintage.com'  # Replace with your email address
        recipient_list = 'sales@masterpiecevintage.com'  # Replace with the recipient's email address

        # Call the send_email function to send the email
        send_email(from_email, 'numberone123123ana.', recipient_list, subject, email_message)

        # Return a JSON response with a success message.
        return JsonResponse({'message': 'Feedback submitted successfully'})

    return render(request, 'feedback.html',
                  {'brands': brands, 'cars_by_brand': cars_by_brand, 'car_list': cars})


def copyindex(request):
    cars = Car.objects.all()

    # Create a dictionary to store cars grouped by brand
    cars_by_brand = {}

    for car in cars:
        brand = car.brand

        if brand not in cars_by_brand:
            cars_by_brand[brand] = []
        cars_by_brand[brand].append(car)

    # Get a list of all unique brand names
    brands = list(cars_by_brand.keys())

    return render(request, 'main.html',
                  {'brands': brands, 'cars_by_brand': cars_by_brand, 'car_list': cars})


class CarAdmin(admin.ModelAdmin):
    # Specify the fields you want to display in the admin form
    list_display = ('brand', 'model', 'price', 'year')

    # Customize the form for adding new listings
    fieldsets = (
        (None, {
            'fields': ('brand', 'model', 'price', 'year', 'main_photo', 'photos', 'short_info')
        }),
    )


def car_details(request, car_id):
    cars = Car.objects.all()
    try:
        car = Car.objects.get(id=car_id)
        car_photos = car.carphoto_set.all()  # Assuming you haven't customized the related name
        photo_count = car_photos.count()
        photo_count += 2
    except Car.DoesNotExist:
        # Handle the case where the car with the specified ID does not exist
        # You can return a 404 error page or a custom error message
        return render(request, 'car_not_found.html')

    return render(request, 'car_details.html',
                  {'car': car, 'car_photos': car_photos, 'photo_count': photo_count, 'car_list': cars})


def contact(request):
    return render(request, 'contact.html')


def car_finder(request):
    return render(request, 'car-finder.html')


def blog(request):
    return render(request, 'news.html')


def sold_cars(request):
    cars = Car.objects.all()
    cars_by_brand = {}  # Your existing logic for grouping by brand

    # Extract parameters from the query string
    price_gteq = request.GET.get('q[price_gteq]')
    price_lteq = request.GET.get('q[price_lteq]')
    make_eq = request.GET.get('q[make_eq]')
    search_cont = request.GET.get('q[ftx_search_cont]')
    year_filter = request.GET.get('q[year_eq]')

    # Apply filters based on the extracted parameters
    if price_gteq and price_lteq:
        cars = cars.filter(price__gte=price_gteq, price__lte=price_lteq)

    if make_eq:
        cars = cars.filter(brand=make_eq)

    if search_cont:
        # Adjust this based on your model fields for searching
        cars = cars.filter(Q(brand__icontains=search_cont) | Q(model__icontains=search_cont))

    if year_filter:
        # Adjust this based on your model field for the year
        cars = cars.filter(year=year_filter)

    # Your existing logic for grouping by brand
    for car in cars:
        brand = car.brand
        if brand not in cars_by_brand:
            cars_by_brand[brand] = []
        cars_by_brand[brand].append(car)

    brands = list(cars_by_brand.keys())

    # Your existing logic for rendering the template
    return render(request, 'sold.html', {'brands': brands, 'cars_by_brand': cars_by_brand, 'car_list': cars})


def testimonials(request):
    return render(request, 'testimonials.html')


def about(request):
    return render(request, 'about.html')
