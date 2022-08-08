from django.shortcuts import render,redirect
from .forms import RegistrationForm,UserForm,UserProfileForm
from .models import Account,UserProfile
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from carts.models import Cart,CartItem
from carts.views import _cart_id
from store.models import Variation
import requests
from orders.models import Order,OrderProduct,Payment
from django.core.paginator import Paginator

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
      first_name    = form.cleaned_data['first_name']
      last_name     = form.cleaned_data['last_name']
      email         = form.cleaned_data['email']
      phone_number  = form.cleaned_data['phone_number']
      password      = form.cleaned_data['password']
      username      = email.split('@')[0]


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

      sender    = 'gkorigin26@gmail.com'
      password  = 'kbdjhjffkihmcfxx'
      receiver  = email
      message   = 'Subject: {}\n\n{}'.format(mail_subject, message_body)
      context   = ssl.create_default_context()

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
      try:
        ex_cart_items = CartItem.objects.filter(user=user)
        if ex_cart_items.exists():
          ex_variation_list = [] 
          ids = []
          for items in ex_cart_items:
            variation = list(items.variation.all())
            if len(variation)>0 :
              ex_variation_list.append(variation)
              ids.append(items.id)
            

          print('ex_variation_list',ex_variation_list)

          cart = Cart.objects.get(cart_id=_cart_id(request))
          cart_items = CartItem.objects.filter(cart=cart)
          for item in cart_items:
            variation = list(item.variation.all())
            if variation in ex_variation_list:
              ex_item_index = ex_variation_list.index(variation)
              ex_item_id = ids[ex_item_index]
              ex_item = CartItem.objects.get(id=ex_item_id)
              ex_item.quantity += item.quantity
              ex_item.save()
            else:
              try:
                cart_item = CartItem.objects.get(product=item.product,user=user)
                cart_item.quantity += item.quantity
                cart_item.save()
              except:
                item.user = user
                item.save()

        else:
          cart = Cart.objects.get(cart_id=_cart_id(request))
          cart_items = CartItem.objects.filter(cart=cart)
          if cart_items.exists():
            for cart_item in cart_items:
              cart_item.user = user
              cart_item.save()
      except:
        pass
      auth.login(request,user)
      # messages.success(request,'You are successfully logged in.')
      
      url = request.META.get('HTTP_REFERER')
      try:
        query = requests.utils.urlparse(url).query
        params = dict(x.split('=') for x in query.split('&'))
        if 'next' in params:
          nextPage = params['next']
          return redirect(nextPage)
      except:
        return redirect('dashboard')
  
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
  paid_orders = Order.objects.filter(user=request.user,is_ordered=True)
  pending_orders = Order.objects.filter(user=request.user,is_ordered=False)
  payments = Payment.objects.filter(user=request.user)
  ordered_products = OrderProduct.objects.filter(user=request.user)
  user_profile  = UserProfile.objects.filter(user=request.user)
  if user_profile.exists():
    user_profile = user_profile[0]
  print(' user is ---->',user_profile)
  context = {
    'paid_orders': paid_orders,
    'paid_orders_count': paid_orders.count(),
    'payments': payments,
    'payments_count': payments.count(),
    'pending_orders': pending_orders,
    'pending_orders_count': pending_orders.count(),
    'ordered_products': ordered_products,
    'user_profile': user_profile
  }
  return render(request, 'accounts/dashboard.html',context)


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


@login_required(login_url='login')
def my_orders(request):
  orders          = Order.objects.filter(user=request.user)
  paginator       = Paginator(orders,10)
  page            = request.GET.get('page')
  paged_orders    = paginator.get_page(page)
  context = {
    'orders': paged_orders,
    'order_counts': orders.count()
  }
  return render(request, 'accounts/myorders.html', context)


@login_required(login_url='login')
def my_payments(request):
  payments          = Payment.objects.filter(user=request.user)
  paginator         = Paginator(payments,10)
  page              = request.GET.get('page')
  paged_payments    = paginator.get_page(page)
  context = {
    'payments'          : paged_payments,
    'payment_counts'    : payments.count(),
  }
  return render(request, 'accounts/mypayments.html', context)


@login_required(login_url='login')
def update_profile(request):
  if request.method == 'POST':
    try:
      user_profile = UserProfile.objects.get(user=request.user)
      user_profile_form = UserProfileForm(request.POST,request.FILES,instance=user_profile)
    except:
      print('EXCEPTION OCCURED')
      user_profile = UserProfile.objects.create(user_id=request.POST.get('user_id'))
      user_profile_form = UserProfileForm(request.POST,request.FILES,instance=user_profile)

    user_form = UserForm(request.POST,instance=request.user)
    if user_form.is_valid() and user_profile_form.is_valid():
      user_form.save()
      user_profile_form.save()
      messages.success(request,'Profile updated successfully')
      return redirect('update_profile')
  
  try:
    user_profile = UserProfile.objects.get(user=request.user)
  except:
    user_profile = None
  context = {
    'user_profile':user_profile
  }
  return render(request, 'accounts/update_profile.html',context)


@login_required(login_url='login')
def change_password(request):
  if request.method == 'POST':
    old_password = request.POST.get('old_password')
    new_password = request.POST.get('new_password')
    confirm_password = request.POST.get('confirm_password')

    if new_password == confirm_password:
      user = Account.objects.get(username__exact=request.user.username)

      if user.check_password(old_password):
        user.set_password(new_password)
        user.save()
        messages.success(request,'Your Password has been changed successfully')
        return redirect('change_password')
      else:
        messages.error(request,'Old password is incorrect')
        return redirect('change_password')
    else:
      messages.error(request,'new password and confirm password are not same')
      return redirect('change_password')

  return render(request, 'accounts/change_password.html')