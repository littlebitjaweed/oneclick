from datetime import datetime
import json
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .razor import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET, client

import razorpay
from .utils import send_otp, check_otp
from .forms import AvailabilityForm, SignUpForm, ProfileForm, EventForm, SellerUpgradeForm, SellerApplicationForm, OTPForm
from .models import Order, Profile, Event, AvailableDate, OTP
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.views.generic import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse


# Create your views here.
def about(request):
    return render(request, 'app/about.html', {})

def home(request):
    categories = [
        {"name": "dIY", "image": "diy.jpg"},
        {"name": "crafts", "image": "craft.jpg"},
        {"name": "adventure", "image": "adventure.jpg"},
        {"name": "sports", "image": "sports.jpg"},
        {"name": "food", "image": "food.jpg"},
        
    ]
    
    featured_events = Event.objects.all().order_by('-created_at')[:3]
    return render(request, 'app/home.html', context={'featured_events': featured_events, 'categories': categories})


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone_number = form.cleaned_data.get('phone_no')

            if not phone_number:
                messages.error(request, "Phone number missing.")
                return redirect('signup')
            send_otp(phone_number)
            request.session['phone_number'] = phone_number  # temporarily store
            return redirect('verify_otp')
    else:
        form = SignUpForm()
    return render(request, 'app/signup.html', context={'form': form})



def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            messages.success(request, ' Login Successful')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'Invalid username or password')
    return render(request, 'app/signin.html', context={})



def logout_view(request):
    logout(request)
    return redirect('home')



def is_seller(user):
    return user.is_authenticated and user.profile.is_seller



@login_required
@user_passes_test(is_seller, login_url="/no-access/")
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.seller = request.user
            event.save()
            return redirect(event.get_absolute_url())
        else:
            print(form.errors)
    else:
        form = EventForm()

    return render(request, "app/create_event.html", {"form": form}) 



class EventDetailView(DetailView):
    model = Event
    template_name = 'app/event_page.html'



def event_page(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'app/event_page.html', {'event': event})



def category_view(request, category_name):
    events = Event.objects.filter(category=category_name)
    return render(request, 'app/category_page.html', {'events': events, 'category_name':category_name})


@login_required
def upgrade_seller(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    profile.is_seller = True
    profile.save()
    messages.success(request, f'{profile.user.username} has been approved as a seller.')
    return redirect('admin_dashboard')  # Adjust the redirect URL


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('signup')
    profile = Profile.objects.get(user=request.user)
    seller_events = Event.objects.filter(seller=request.user)
    return render(request, 'app/dashboard.html', {"profile":profile, "seller_events":seller_events})



@login_required
def update_profile(request):
    user = request.user

    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():

            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            form.save()

            return redirect("dashboard")
        
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'app/profile.html', context={'form': form})


def seller_application_view(request):
    if request.method == 'POST':
        form = SellerApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, "Your application has been submitted for review.")
            return redirect('dashboard')
    else:
        form = SellerApplicationForm()
    return render(request, 'app/seller.html', {'form': form})



@login_required
def payment_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        participants = int(request.POST.get('participants'))
        selected_date = request.POST.get('selected_date')
        selected_date = datetime.strptime(selected_date, '%B %d, %Y').date()


    
        base_price = event.price * participants
        convenience_fee = event.convenience_fee
        gst_amount = (base_price + convenience_fee) * (event.gst_percentage / 100)
        total_price = base_price + convenience_fee + gst_amount

        # Store order in the database
        order = Order.objects.create(
            user=request.user,
            event=event,
            participants=participants,
            selected_date=selected_date,
            total_price=total_price
        )
        return render(request, 'app/payment_success.html', {'order': order})
    else:
        return redirect('availability', event_id=event_id)
    



def verify_otp_view(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        phone = request.session.get('phone_number')
        
        if check_otp(phone, otp) == 'approved':
            # log user in or mark as verified
            messages.success(request, "Phone number verified!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid OTP. Try again.")
    
    return render(request, 'app/verify_otp.html')

def available_page(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    form = AvailabilityForm(event=event)

    base_price = gst_amount = total_price = None
    convenience_fee = event.convenience_fee
    participants = None

    if request.method == 'POST':
        form = AvailabilityForm(request.POST, event=event)
        if form.is_valid():
            participants = form.cleaned_data['participants']
            selected_date = form.cleaned_data['selected_date']

            base_price = event.price * participants
            gst_amount = (base_price + convenience_fee) * (event.gst_percentage / 100)
            total_price = base_price + convenience_fee + gst_amount

            return render(request, 'app/available.html', {
                'event': event,
                'form': form,
                'base_price': base_price,
                'convenience_fee': convenience_fee,
                'gst_amount': gst_amount,
                'total_price': total_price,
                'participants': participants,
                'selected_date': selected_date
            })

    return render(request, 'app/available.html', {
        'event': event,
        'form': form,
        'base_price': base_price,
        'convenience_fee': convenience_fee,
        'gst_amount': gst_amount,
        'total_price': total_price,
        'participants': participants,
        'RAZORPAY_API_KEY':settings.RAZORPAY_KEY_ID,
    })

@csrf_exempt  # Only for testing, use proper CSRF in production
def create_payment(request):
    if request.method == "POST":
        amount = int(request.POST.get("amount")) * 100  # Razorpay uses paise (multiply by 100)
        currency = "INR"
        
        payment_data = {
            "amount": amount,
            "currency": currency,
            "receipt": "receipt#1",
            "payment_capture": 1  # Auto-capture payment
        }
        
        try:
            order = client.order.create(data=payment_data)
            return JsonResponse({"order_id": order["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        razorpay_order_id = request.POST.get("razorpay_order_id")
        razorpay_signature = request.POST.get("razorpay_signature")
        
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        
        try:
            client.utility.verify_payment_signature(params_dict)
            return JsonResponse({"status": "success"})
        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({"status": "failed"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def create_razorpay_order(request):
    if request.method == 'POST':
        try:
            client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
            
            # Get amount from request
            data = json.loads(request.body)
            amount = int(data['amount'])
            
            # Create order
            payment_data = {
                'amount': amount,
                'currency': 'INR',
                'payment_capture': 1
            }
            order = client.order.create(payment_data)
            
            return JsonResponse({
                'order_id': order['id'],
                'amount': order['amount']
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
