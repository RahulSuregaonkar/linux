import json

from account.models import Address
from basket.basket import Basket
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from store.models import Product
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from orders.views import payment_confirmation

from django.contrib.postgres.search import SearchVector
from .models import DeliveryOptions
import stripe


@login_required
def deliverychoices(request):
    if 'q' in request.GET:
        q = request.GET['q']
        data = Product.objects.annotate(search = SearchVector('title', 'author'),).filter(search=q)
        return render(request, 'store/product_page.html', {'products': data})
    
    
    deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
    return render(request, "checkout/delivery_choices.html", {"deliveryoptions": deliveryoptions})


@login_required
def basket_update_delivery(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        delivery_option = int(request.POST.get("deliveryoption"))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)
        updated_total_price = basket.basket_update_delivery(delivery_type.delivery_price)

        session = request.session
        if "purchase" not in request.session:
            session["purchase"] = {
                "delivery_id": delivery_type.id,
            }
        else:
            session["purchase"]["delivery_id"] = delivery_type.id
            session.modified = True

        response = JsonResponse({"total": updated_total_price, "delivery_price": delivery_type.delivery_price})
        return response

@login_required
def set_delivery_address(request):
    if 'q' in request.GET:
        q = request.GET['q']
        data = Product.objects.annotate(search = SearchVector('title', 'author'),).filter(search=q)
        return render(request, 'store/product_page.html', {'products': data})
    
    if "purchase" not in request.session:
        messages.success(request, "Please select delivery option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    addresses = Address.objects.filter(customer=request.user).order_by("-default")
    

    return render(request, "checkout/set_delivery_address.html", {"addresses": addresses})


   
@login_required
def delivery_address(request):
    if 'q' in request.GET:
        q = request.GET['q']
        data = Product.objects.annotate(search = SearchVector('title', 'author'),).filter(search=q)
        return render(request, 'store/product_page.html', {'products': data})
    
    
    session = request.session
    if "purchase" not in request.session:
        messages.success(request, "Please select delivery option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    addresses = Address.objects.filter(customer=request.user).order_by("-default")
    
   
    if "address" not in request.session:
        session["address"] = {"address_id": str(addresses[0].id)}
    else:
        session["address"]["address_id"] = str(addresses[0].id)
        session.modified = True


    return render(request, "checkout/delivery_address.html", {"addresses": addresses})


@login_required
def payment_selection(request):
    addresses = Address.objects.filter(customer=request.user, default=True)
    
    if 'q' in request.GET:
        q = request.GET['q']
        data = Product.objects.annotate(search = SearchVector('title', 'author'),).filter(search=q)
        return render(request, 'store/product_page.html', {'products': data})
    
    
    basket = Basket(request)
    total = str(basket.get_total_price())
    total = total.replace('.', '')
    total = int(total)
    print(total)

    stripe.api_key = 'sk_test_51Ngp9lSD595QLxWl8MBGSBLsRICe2ZTg1uBbSKj84QL317bEuFaLy2wWzWyti3Nykdmyieqvgd5COWFk4HsyYUAD0088IBTohA'
    
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='inr',
        metadata={'userid': request.user.id}
    )


    return render(request, "checkout/payment_selection.html", {'client_secret': intent.client_secret,"addresses": addresses})




@login_required
def payment_successful(request):
    basket = Basket(request)
    basket.clear()
    return render(request, "checkout/payment_successful.html", {})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)