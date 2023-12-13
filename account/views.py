from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse,  HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from orders.views import user_orders
from django.contrib import messages
from django.contrib.postgres.search import SearchVector

from .forms import RegistrationForm, UserEditForm, UserProfileForm, UserAddressForm
from .models import Customer, Profile, Address
from .tokens import account_activation_token
from store.models import Product
from .tokens import account_activation_token
from orders.views import user_orders
from orders.models import Order
from sellbook.forms import NewSellingForm
from sellbook.models import sell_old_books, Category
from django.utils.text import slugify
from django.db.models import Sum
from datetime import datetime, timedelta


@login_required
def wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user)
    return render(request, "account/dashboard/user_wish_list.html", {"wishlist": products})


@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(request, product.title +
                         " has been removed from your WishList")
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, "item Added " +
                         product.title + " to your WishList")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def profile(request):
    return render(request, 'account/dashboard/profile.html')


@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request,
                  'account/dashboard/dashboard.html',
                  {'section': 'profile', 'orders': orders})


@login_required
def user_orders(request):
    user_id = request.user.id
    addresses = Address.objects.filter(customer=request.user, default=True)
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    selling_form = None
    category = Category.objects.all()
    new_orders = 0

    if request.method == "POST":
        six_months = datetime.now() - timedelta(days=182)
        new_orders = Order.objects.filter(
            billing_status="True", id=request.POST['selling_prod'], created__gte=six_months)
        id1 = request.POST['selling_prod']
        print(id1)
        print(len(new_orders))
        if len(new_orders) == 1:
            pass
        else:
            return HttpResponse("you cannot sell the book it shad exceeded the time limit of 6 monrths")

    if request.method == "POST":
        quantity = request.POST['quantity']
        real_quantity = request.POST['real_quantity']

        if quantity > real_quantity:
            return HttpResponse('You cannot sell more books than ordered')

    if request.method == "POST" and request.POST['quantity'] == request.POST['real_quantity']:
        title = request.POST['title']

        sell = sell_old_books.objects.filter(
            selling_prod=request.POST['selling_prod'], selling_user=request.POST['selling_user']).exists()
        if sell == True:
            return HttpResponse('hey the product is already in the selling list')

        sell_form = NewSellingForm(request.POST, request.FILES)
        regular_1 = (float(request.POST['regular_price']))/2
        if sell_form.is_valid():
            selling_form = sell_form.save(commit=False)
            selling_form.title = title
            selling_form.user_id = request.user.id
            selling_form.regular_price = request.POST['regular_price']
            selling_form.slug = slugify(selling_form.description + selling_form.regular_price +
                                        request.POST['selling_prod'] + request.POST['selling_user'])
            selling_form.discount_price = regular_1
            selling_form.save()
            messages.success(request,"successfully added the book in the selling list")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        sell_form = NewSellingForm()

    if request.method == "POST" and request.POST['quantity'] == '1' and request.POST['real_quantity'] == '2':
        title = request.POST['title']
        sell = sell_old_books.objects.filter(selling_prod=request.POST['selling_prod'], selling_user=request.POST[
            'selling_user'], quantity=request.POST['real_quantity'], real_quantity=request.POST['real_quantity']).exists()
        if sell == True:
            return HttpResponse('hey the product is already in the selling object')

        sell = sell_old_books.objects.filter(
            selling_prod=request.POST['selling_prod'], selling_user=request.POST['selling_user'], quantity=request.POST['quantity'] == '1').count()
        if not sell <= 1:
            return HttpResponse('you have sold both the products and already')

        sell_form = NewSellingForm(request.POST, request.FILES)
        regular_1 = (float(request.POST['regular_price']))/4
        real_price = (float(request.POST['regular_price']))/2

        if sell_form.is_valid():
            selling_form = sell_form.save(commit=False)
            selling_form.user_id = request.user.id
            selling_form.title = title
            selling_form.regular_price = real_price
            selling_form.slug = slugify(
                selling_form.description + request.POST['regular_price'] + request.POST['selling_prod'] + request.POST['selling_user'])
            selling_form.discount_price = regular_1
            selling_form.save()
            messages.success(request,"successfully added the book in the selling list")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        sell_form = NewSellingForm()

    if request.method == "POST" and request.POST['quantity'] == '1' and request.POST['real_quantity'] == '3':
        title = request.POST['title']

        sell = sell_old_books.objects.filter(
            selling_prod=request.POST['selling_prod'], selling_user=request.POST['selling_user']).aggregate(TOTAL=Sum('quantity'))['TOTAL']
        print(sell)
        if sell == None:
            sell = 0

        if not sell <= 2:
            return HttpResponse('sold all 3 books already')

        sell_form = NewSellingForm(request.POST, request.FILES)
        regular_1 = (float(request.POST['regular_price']))/6
        real_price = regular_1*2

        if sell_form.is_valid():
            selling_form = sell_form.save(commit=False)
            selling_form.user_id = request.user.id
            selling_form.title = title
            selling_form.regular_price = real_price
            selling_form.slug = slugify(
                selling_form.description + request.POST['regular_price'] + request.POST['selling_prod'] + request.POST['selling_user'])
            selling_form.discount_price = regular_1
            selling_form.save()
            messages.success(request,"successfully added the book in the selling list")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        sell_form = NewSellingForm()

    if request.method == "POST" and request.POST['quantity'] == '2' and request.POST['real_quantity'] == '3':
        title = request.POST['title']
        sell = sell_old_books.objects.filter(
            selling_prod=request.POST['selling_prod'], selling_user=request.POST['selling_user']).aggregate(TOTAL=Sum('quantity'))['TOTAL']
        print(sell)
        if sell == None:
            sell = 0

        if not sell < 2:
            return HttpResponse('sold all 3 books already')

        sell_form = NewSellingForm(request.POST, request.FILES)
        regular_1 = (float(request.POST['regular_price']))/3
        real_price = regular_1*2

        if sell_form.is_valid():
            selling_form = sell_form.save(commit=False)
            selling_form.user_id = request.user.id
            selling_form.title = title
            selling_form.regular_price = real_price
            selling_form.slug = slugify(
                selling_form.description + request.POST['regular_price'] + request.POST['selling_prod'] + request.POST['selling_user'])
            selling_form.discount_price = regular_1
            selling_form.save()
            messages.success(request,"successfully added the book in the selling list")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        sell_form = NewSellingForm()

    if request.method == "POST" and request.POST['quantity'] == '1' and request.POST['real_quantity'] == '4':

        title = request.POST['title']
        sell = sell_old_books.objects.filter(
            selling_prod=request.POST['selling_prod'], selling_user=request.POST['selling_user']).aggregate(TOTAL=Sum('quantity'))['TOTAL']

        if sell == None:
            sell = 0

        if not sell <= 3:
            print(sell)
            return HttpResponse('sold all  books already')

        sell_form = NewSellingForm(request.POST, request.FILES)
        regular_1 = (float(request.POST['regular_price']))/8
        real_price = regular_1*2

        if sell_form.is_valid():
            selling_form = sell_form.save(commit=False)
            selling_form.user_id = request.user.id
            selling_form.title = title
            selling_form.regular_price = real_price
            selling_form.slug = slugify(
                selling_form.description + request.POST['regular_price'] + request.POST['selling_prod'] + request.POST['selling_user'])
            selling_form.discount_price = regular_1
            selling_form.save()
            messages.success(request,"successfully added the book in the selling list")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        sell_form = NewSellingForm()

    if request.method == "POST" and request.POST['quantity'] == '2' and request.POST['real_quantity'] == '4':

        title = request.POST['title']
        sell = sell_old_books.objects.filter(
            selling_prod=request.POST['selling_prod'], selling_user=request.POST['selling_user']).aggregate(TOTAL=Sum('quantity'))['TOTAL']

        if sell == None:
            sell = 0

        if not sell < 3:
            print(sell)
            return HttpResponse('sold all 3 books already')

        sell_form = NewSellingForm(request.POST, request.FILES)
        regular_1 = (float(request.POST['regular_price']))/4
        real_price = regular_1*2

        if sell_form.is_valid():
            selling_form = sell_form.save(commit=False)
            selling_form.user_id = request.user.id
            selling_form.title = title
            selling_form.regular_price = real_price
            selling_form.slug = slugify(
                selling_form.description + request.POST['regular_price'] + request.POST['selling_prod'] + request.POST['selling_user'])
            selling_form.discount_price = regular_1
            selling_form.save()
            messages.success(request,"successfully added the book in the selling list")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        sell_form = NewSellingForm()

    if request.method == "POST" and request.POST['quantity'] == '3' and request.POST['real_quantity'] == '4':

        title = request.POST['title']

        sell = sell_old_books.objects.filter(
            selling_prod=request.POST['selling_prod'], selling_user=request.POST['selling_user']).aggregate(TOTAL=Sum('quantity'))['TOTAL']
        if sell == None:
            sell = 0

        print(sell)
        if not sell < 2:

            return HttpResponse('sold all 3 books already')

        sell_form = NewSellingForm(request.POST, request.FILES)
        regular_1 = ((float(request.POST['regular_price']))/4)
        regular_2 = ((regular_1*3))/2
        real_price = regular_2*2

        if sell_form.is_valid():
            selling_form = sell_form.save(commit=False)
            selling_form.user_id = request.user.id
            selling_form.title = title
            selling_form.regular_price = real_price
            selling_form.slug = slugify(
                selling_form.description + request.POST['regular_price'] + request.POST['selling_prod'] + request.POST['selling_user'])
            selling_form.discount_price = regular_2
            selling_form.save()
            messages.success(request,"successfully added the book in the selling list")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    else:
        sell_form = NewSellingForm()

    return render(request, "account/dashboard/user_orders.html", {"orders": orders, "addresses": addresses, 'selling_form': selling_form, 'sell_form': sell_form, 'categories': category, 'new_orders': new_orders})


@login_required
def edit_details(request):

    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)

    return render(request, 'account/dashboard/edit_details.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def delete_user(request):
    user = Customer.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')


def account_register(request):

    if request.user.is_authenticated:
        return redirect('account:dashboard')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.phone = registerForm.cleaned_data['mobile']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return render(request, 'account/registration/register_email_confirm.html', {'form': registerForm})
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')


# Addresses

@login_required
def view_address(request):
    if 'q' in request.GET:
        q = request.GET['q']
        data = Product.objects.annotate(
            search=SearchVector('title', 'author'),).filter(search=q)
        return render(request, 'store/product_page.html', {'products': data})

    addresses = Address.objects.filter(customer=request.user)
    return render(request, "account/dashboard/addresses.html", {"addresses": addresses})


@login_required
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address_form = UserAddressForm()
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})


@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})


@login_required
def delete_address(request, id):
    address = Address.objects.filter(pk=id, customer=request.user).delete()
    return redirect("account:addresses")


@login_required
def set_default(request, id):
    Address.objects.filter(customer=request.user,
                           default=True).update(default=False)
    Address.objects.filter(pk=id, customer=request.user).update(default=True)

    previous_url = request.META.get("HTTP_REFERER")

    if "delivery_address" in previous_url:
        return redirect("checkout:delivery_address")

    return redirect("account:addresses")


