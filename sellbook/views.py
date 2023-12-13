from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import sell_old_books, Category
from .forms import NewSellingForm, NewSellingEditForm
from orders.models import Order, OrderItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from account.models import Review
from django.db.models import Avg, Min, Max
from store.models import Product
# Create your views here.
def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    data1 = sell_old_books.objects.filter(status="published",category__in=Category.objects.get(
        slug=category_slug).get_descendants(include_self=True))
    page = request.GET.get('page', 1)
    paginator = Paginator(data1, 8)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if 'q' in request.GET:
        q = request.GET['q']
        data = sell_old_books.objects.annotate(
            search=SearchVector('title'),).filter(search=q)
        return render(request, 'oldbooks/index.html', {'products': data})
    else:
        return render(request, 'oldbooks/category.html', {'category': category, 'products': products})

def home(request):
    min_price = sell_old_books.objects.aggregate(Min('discount_price'))['discount_price__min']
    max_price = sell_old_books.objects.aggregate(Max('discount_price'))['discount_price__max']
    
    if 'q' in request.GET:
        q = request.GET['q']
        data = sell_old_books.objects.annotate(
            search=SearchVector('title'),).filter(search=q)

    else:
        data1 = sell_old_books.objects.filter(status='published')
        page = request.GET.get('page', 1)
        paginator = Paginator(data1, 8)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
    return render(request, 'oldbooks/index.html', {'products' : data, 'min': min_price, 'max': max_price})

def product_detail(request, slug):

    product = get_object_or_404(sell_old_books,slug=slug,status='published')
    p = sell_old_books.objects.filter(slug=slug).values_list('title').first()
    print(str(p))
    products = Product.objects.annotate(search=SearchVector('title'),).filter(search=p).first()
    print(products)
    average_rating = Review.objects.filter(
        post=products).aggregate(Avg("rate"))["rate__avg"] or 0
    
    return render(request, 'oldbooks/product_detail.html', {'product': product,'average_rating':average_rating}) 

def product_detail1(request, slug):

    product = get_object_or_404(sell_old_books,slug=slug,status='Sold')
    p = sell_old_books.objects.filter(slug=slug).values_list('title').first()
    print(str(p))
    products = Product.objects.annotate(search=SearchVector('title'),).filter(search=p).first()
    print(products)
    average_rating = Review.objects.filter(
        post=products).aggregate(Avg("rate"))["rate__avg"] or 0
    
    return render(request, 'oldbooks/product_detail1.html', {'product': product,'average_rating':average_rating}) 

@login_required
def mybooks(request):
    if 'q' in request.GET:
        q = request.GET['q']
        data = sell_old_books.objects.annotate(
            search=SearchVector('title'),).filter(search=q)
        return render(request, 'oldbooks/index.html', {'products': data})

    all_posts1 = sell_old_books.objects.filter(user_id=request.user.id,status='published')
    page = request.GET.get('page', 1)
    paginator = Paginator(all_posts1, 8)
    try:
        all_posts = paginator.page(page)
    except PageNotAnInteger:
        all_posts = paginator.page(1)
    except EmptyPage:
        all_posts = paginator.page(paginator.num_pages)

    return render(request, 'oldbooks/mybooks.html', {'products' : all_posts})

@login_required
def edit_books(request,pk):
    sell_book_id = sell_old_books.objects.get(id=pk)
    form = NewSellingEditForm(instance=sell_book_id)
    if request.method == 'POST':
        form = NewSellingEditForm(request.POST,request.FILES, instance=sell_book_id)
        if form.is_valid():
            form.save()
            messages.success(request, "details successfully Updated")
            return redirect('sellbook:mybooks')
    else:
        form = NewSellingEditForm(instance=sell_book_id)
    context = {'form':form}
    return render(request, 'oldbooks/edit.html', context)

@login_required
def delete_books(request,pk):
    form = sell_old_books.objects.get(id=pk)
    form.delete()
    messages.info(request,"book has been deleted successfully")
    return redirect('sellbook:mybooks')

@login_required
def mysoldbooks(request):
    if 'q' in request.GET:
        q = request.GET['q']
        data = sell_old_books.objects.annotate(
            search=SearchVector('title'),).filter(search=q)
        return render(request, 'oldbooks/index.html', {'products': data})

    all_posts1 = sell_old_books.objects.filter(user_id=request.user.id,status='Sold')
    page = request.GET.get('page', 1)
    paginator = Paginator(all_posts1, 8)
    try:
        all_posts = paginator.page(page)
    except PageNotAnInteger:
        all_posts = paginator.page(1)
    except EmptyPage:
        all_posts = paginator.page(paginator.num_pages)
    

    return render(request, 'oldbooks/mysoldbooks.html', {'products' : all_posts})