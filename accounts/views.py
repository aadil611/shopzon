from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

# lib for email verificatiron
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
import smtplib,ssl

# Create your views here.
def register(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      email = form.cleaned_data['email']
      phone_number = form.cleaned_data['phone_number']
      password = form.cleaned_data['password']
      username = email.split('@')[0]


      user = Account.objects.create(first_name=first_name,username=username, last_name=last_name, email=email)
      user.phone_number = phone_number
      user.set_password(password)
      user.save()

      # user activation  
      current_site = get_current_site(request)
      mail_subject = 'Please activate your account'
      message_body = render_to_string('accounts/account_verification.html',{
        'user':user,
        'domain':current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
      })

      sender = 'gkorigin26@gmail.com'
      password = 'kbdjhjffkihmcfxx'
      receiver = email 
      message = 'Subject: {}\n\n{}'.format(mail_subject, message_body)
      context = ssl.create_default_context()

      with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as server:
        server.login(sender,password)
        server.sendmail(sender,receiver,message)

      return redirect('/accounts/login/?command=verification&email='+email)
  else:
    form = RegistrationForm()

  if form.errors.get('email',False):
    messages.error(request,form.errors.get('email',False)[0])
  if form.errors.get('password',False):
    messages.error(request,'password does not match')
  context = {'form': form}
  return render(request,'accounts/login_register.html',context)

def login(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = auth.authenticate(username=username, password=password)

    if user is None:
      messages.error(request,'username or password is incorrect')
    else:
      auth.login(request,user)
      # messages.success(request,'You are successfully logged in.')
      return redirect('home')
  
  return render(request,'accounts/login_register.html')


def activate(request,uid64,token):
  try:
    uid = urlsafe_base64_decode(uid64).decode()
    user = Account._default_manager.get(id=uid)
  except (ValueError,TypeError,OverflowError,Account.DoesNotExist):
    user = None

  if user is not None and default_token_generator.check_token(user,token):
    user.is_active = True
    user.save()
    messages.success(request,'your account is verified successfully, You can login now')
    return redirect('login')
  else:
    messages.error(request,'Sorry, this link is expired. Please try again later')
    return redirect('register')


@login_required(login_url='login')
def logout(request):
  auth.logout(request)
  messages.success(request,'you are logged out successfully')
  return redirect('login')


@login_required(login_url='login')
def dashboard(request):
  return render(request, 'accounts/dashboard.html')


def forgot_password(request):
  if request.method == 'POST':
    email = request.POST.get('email')

    if Account.objects.filter(email=email).exists():
      user = Account.objects.get(email__exact=email)

      current_site = get_current_site(request)
      mail_subject = 'Reset your password'
      mail_body    = render_to_string('accounts/reset_password_mail.html',{
        'user'  : user,
        'domain': current_site,
        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user)
      })

      message = 'Subject: {} \n\n {}'.format(mail_subject, mail_body)
      sender = 'gkorigin26@gmail.com'
      password = 'kbdjhjffkihmcfxx'
      receiver = email

      context = ssl.create_default_context()
      with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as server:
        server.login(sender,password)
        server.sendmail(sender,receiver,message)

      messages.success(request,'reset link has been sent to your email')
      return redirect('login')
    else:
      messages.error(request,'Account does not exist for given email')
      return redirect('forgot_password')

  return render(request, 'accounts/forget_password.html')


def reset_password_validate(request,uidb64,token):
  try:
    uid = urlsafe_base64_decode(uidb64).decode()
    user  = Account._default_manager.get(id=uid)
  except:
    user = None
  if user is not None and default_token_generator.check_token(user,token):
    request.session['uid'] = uid
    messages.success(request,'please reset your password')
    return redirect('reset_password')
  else:
    messages.error(request,'this link is expired,please try again')
    return redirect('forgot_password')


def reset_password(request):
  if request.method == 'POST':
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')

    if password == confirm_password:
      uid = request.session.get('uid')
      user = Account.objects.get(id=uid)
      user.set_password(password)
      user.save()
      messages.success(request,'password reset successful, You can login now')
      return redirect('login')
    else:
      messages.error(request,'password does not match, please try again')
      return redirect('reset_password')
  return render(request, 'accounts/reset_password.html')