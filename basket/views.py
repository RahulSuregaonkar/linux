from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store.models import Product
from .models import Save_For_Later

from .basket import Basket
from django.contrib.postgres.search import SearchVector

@login_required
def basket_summary(request):
    if 'q' in request.GET:
        q = request.GET['q']
        data = Product.objects.annotate(search = SearchVector('title', 'author'),).filter(search=q)
        return render(request, 'store/product_page.html', {'products': data})

    basket = Basket(request)
    products = Save_For_Later.objects.filter(user=request.user)
   
    return render(request, 'basket/summary.html', {'basket': basket, 'save_for_later':products})

@login_required
def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)

        basketqty = basket.__len__()
        response = JsonResponse({'qty': basketqty})
        return response

@login_required
def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.delete(product=product_id)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response

@login_required
def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product=product_id, qty=product_qty)

        basketqty = basket.__len__()
        basketsubtotal = basket.get_subtotal_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': basketsubtotal})
        return response





@login_required
def add_to_save_for_later(request, id):
    product = get_object_or_404(Product, pk=id)
    quantity = request.GET.get('quantity')
    created = Save_For_Later.objects.create(
        product=product,
        user=request.user,
        quantity=quantity
    )
    basket = Basket(request)
    basket.delete(product=id)
    if created:
        messages.success(request,product.title + "item has been added to ")


    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def remove_save_for_later(request,id,id2):
    quantity = request.GET.get('quantity')
    product = get_object_or_404(Product, pk=id2)
    obj = get_object_or_404(Save_For_Later,pk=id,user=request.user,product=product, quantity=quantity)
    removed=obj.delete()
    
    
    if removed:
        messages.success(request,product.title + "item has been removed from the ")
        
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    