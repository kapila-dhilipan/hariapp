from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views import View
from django.core.mail import send_mail
from utils.email_task import send_contact_mail
from django.conf import settings
import json
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from .forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from .models import Tracker
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from datetime import timedelta
from django.contrib.auth.models import AnonymousUser

# Create your views here.

def portfolio(request):
    
    if settings.TRACKER_ON:
    # Integrating the Tracker function
      tracker = Tracker.objects.create_from_request(request)
      tracker.save()
    return render(request, 'portfolio.html')
    
def contact_mail(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode("utf-8"))
        print(json.dumps(json_data, indent=2))
        # Access individual fields
        full_name = json_data.get('full_name', '')
        email = json_data.get('email', '')
        mobile_number = json_data.get('mobile_number', '')
        email_subject = json_data.get('email_subject', '')
        message = json_data.get('message', '')
        try:
            email_body = f"From: {full_name}\n"
            if email:
                email_body += f"Email: {email}\n"
            if mobile_number:
                email_body += f"Mobile Number: {mobile_number}\n"
            email_body += f"\n{message}"

            send_mail(
                subject=email_subject,
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['harijordan95@gmail.com'],
            )

            return JsonResponse({'success': 'Email sent successfully!'})
        except Exception as e:
            # Handle exceptions, log them, or customize the response as needed
            return JsonResponse({'error': str(e)}, status=500)


# Pages
def count_visitors(queryset, start_date, end_date):
    return queryset.filter(timestamp__date__range=[start_date, end_date]).count()

def get_monthly_chart_data(all_trackers):
    current_month = timezone.now().month
        
    months_count_chart = all_trackers.filter(
        timestamp__isnull=False,
        timestamp__gte=timezone.now() - relativedelta(months=10),
    ).annotate(
        month=ExtractMonth('timestamp')
    ).values('month').annotate(count=Count('id'))

    month_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_dict = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12,
    }

    month_keys = list(month_list[current_month - 10:] + month_list[:current_month])
    
    chart_data = {}
    for month_key in month_keys:
        month_value = month_dict[month_key]
        found_data = next((data for data in months_count_chart if data["month"] == month_value), None)
        chart_data[month_key] = found_data["count"] if found_data else 0

    return chart_data

@login_required
def Dashboard(request):
    if settings.TRACKER_ON and request.user.is_authenticated:
        final_user = str(request.user)
        try:
            tracker, created = Tracker.objects.get_or_create(ip_address=request.META['REMOTE_ADDR'])
            if not created and tracker.user is None:
                if not isinstance(request.user, AnonymousUser):
                    tracker.user = final_user
                    tracker.save()
        except Tracker.MultipleObjectsReturned:
            trackers = Tracker.objects.filter(ip_address=request.META['REMOTE_ADDR'], user="AnonymousUser").update(user=final_user)

    # Retrieve all instances of the Tracker model
    all_trackers = Tracker.objects.all()

    # Total visitors
    total_visitors = all_trackers.count()

    # Today's visitors
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    todays_visitors = count_visitors(all_trackers, today, today)
    yesterdays_visitors = count_visitors(all_trackers, yesterday, yesterday)

    # Monthly chart data
    chart_data = get_monthly_chart_data(all_trackers)

    # Calculate the number of visitors for the current month
    current_month = timezone.now().month
    first_day_of_current_month = today.replace(day=1)
    last_day_of_current_month = (first_day_of_current_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    monthly_visitors = count_visitors(all_trackers, first_day_of_current_month, last_day_of_current_month)
    
    # Calculate the number of visitors for the previous month
    first_day_of_previous_month = (first_day_of_current_month - timedelta(days=1)).replace(day=1)
    last_day_of_previous_month = (first_day_of_current_month - timedelta(days=1)).replace(day=31)
    previous_month_visitors = count_visitors(all_trackers, first_day_of_previous_month, last_day_of_previous_month)
   
    # Calculate the percentage increase
    percentage_increase_today = (todays_visitors - yesterdays_visitors) / (yesterdays_visitors or 1) * 100
    percentage_increase_monthly = (monthly_visitors) / (previous_month_visitors or 1) * 100

    context = {
        'segment': 'index',
        'total_visitors': total_visitors,
        'todays_visitors': todays_visitors,
        'percentage_increase_today': percentage_increase_today,
        'percentage_increase_monthly': percentage_increase_monthly,
        'all_trackers': all_trackers,
        'chart_data': chart_data,
    }
    
    return render(request, 'pages/index.html', context=context)

def billing(request):
  
  return render(request, 'pages/billing.html', { 'segment': 'billing' })

def tables(request):
  return render(request, 'pages/tables.html', { 'segment': 'tables' })

def vr(request):
  return render(request, 'pages/virtual-reality.html', { 'segment': 'vr' })

def rtl(request):
  return render(request, 'pages/rtl.html', { 'segment': 'rtl' })

def profile(request):
  return render(request, 'pages/profile.html', { 'segment': 'profile' })


# Authentication
class UserLoginView(LoginView):
  template_name = 'accounts/login.html'
  form_class = LoginForm

def register(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      print('Account created successfully!')
      return redirect('/accounts/login/')
    else:
      print("Register failed!")
  else:
    form = RegistrationForm()

  context = { 'form': form }
  return render(request, 'accounts/register.html', context)

def logout_view(request):
  logout(request)
  return redirect('/accounts/login/')

class UserPasswordResetView(PasswordResetView):
  template_name = 'accounts/password_reset.html'
  form_class = UserPasswordResetForm

class UserPasswordResetConfirmView(PasswordResetConfirmView):
  template_name = 'accounts/password_reset_confirm.html'
  form_class = UserSetPasswordForm

class UserPasswordChangeView(PasswordChangeView):
  template_name = 'accounts/password_change.html'
  form_class = UserPasswordChangeForm