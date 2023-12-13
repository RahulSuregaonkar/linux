from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from .models import Category, Product,ProductSpecifiactionValue
from django.contrib.postgres.search import SearchVector
from account.models import Profile
from account.models import Review
from account.forms import NewCommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Min, Max
from django.template.loader import render_to_string
from django.http import HttpResponse
import json


def search(request):
    data = []  # Initialize data with an empty list or default value
    min_price = Product.objects.aggregate(Min('discount_price'))['discount_price__min']
    max_price = Product.objects.aggregate(Max('discount_price'))['discount_price__max']
    authors = Product.objects.values_list('author', flat=True).distinct()
    print(authors)
    
    if 'q' in request.GET:
        q = request.GET['q']
        data = Product.objects.annotate(
            search=SearchVector('title', 'author')
        ).filter(search=q)

    if request.method == 'POST' and 'q' in request.POST:
        q = request.POST['q']
        data = Product.objects.filter(title__icontains=q, author__icontains=q)[:10]  # Limit the results to 10

        # Extract relevant information for suggestions (customize based on your Product model)
        suggestions = [{'id': product.author, 'title': product.title} for product in data]
        return JsonResponse({'suggestions': suggestions})

    
    return render(request, 'store/product_page.html', {'products': data,'min': min_price, 'max': max_price, 'authors':authors})

def all_products(request):
    featured = Product.objects.filter(category_id=251)
    new_arrivals = Product.objects.filter(category_id=250)
    limited = Product.objects.filter(category_id=249)
    BestSellers = Product.objects.filter(category_id=252)
    return render(request, 'store/index.html', {'featured': featured, 'new_arrivals': new_arrivals, 'limited': limited, 'BestSellers': BestSellers})


def serialize_products(products, request):
    serialized_products = []
    print(products)
    for product in products:
        featured_image = None

        # Check for the featured image
        for image in product.product_image.all():
            if image.is_feature:
                featured_image = image
                break

        alt_text = featured_image.alt_text if featured_image else ''

        serialized_product = {
            'url': product.get_absolute_url(),
            'image_url': featured_image.image.url if featured_image else '',
            'alt_text': alt_text,
            'title': product.title,
            'discount_price': product.discount_price,
            'regular_price': product.regular_price,
            'discount_percentage': product.discount_percentage,
            'author': product.author,
        }
        serialized_products.append(serialized_product)
    return serialized_products


def all_products_in_product_page(request):
    min_price = Product.objects.aggregate(Min('discount_price'))['discount_price__min']
    max_price = Product.objects.aggregate(Max('discount_price'))['discount_price__max']
    
    authors = Product.objects.values_list('author', flat=True).distinct()
    print(authors)

    # Initialize variables with default values
    selectedCategories = []
    selectedDiscounts = []
    priceRangeValue = ""
    selectedAuthors = []
    selectedLanguages = []

    # Check if the request is an AJAX request
    is_ajax_request = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if is_ajax_request:
        json_data = json.loads(request.body.decode('utf-8'))
        selectedCategories = json_data.get('categories', [])
        print(selectedCategories)
        selectedDiscounts = json_data.get('discountRange', [])
        priceRangeValue = json_data.get('priceRange', "")
        selectedAuthors = json_data.get('authors', [])
        selectedLanguages = json_data.get('languages', [])

    # Filter the products based on selected criteria
    data1 = Product.objects.prefetch_related("product_image").filter(is_active=True)

    # Apply filters as needed, for example:
    if selectedCategories:
        # Create a list of category IDs including descendants
        category_ids_with_descendants = []
        for category_id in selectedCategories:
            category = Category.objects.get(pk=category_id)
            descendants = category.get_descendants(include_self=True)
            category_ids_with_descendants.extend(descendant.pk for descendant in descendants)

        data1 = data1.filter(category_id__in=category_ids_with_descendants)
        print(data1)

    
    if selectedDiscounts:
        data1 = data1.filter(discount_percentage__gte=min(selectedDiscounts))

    if priceRangeValue:
        data1 = data1.filter(discount_price__lte=priceRangeValue)

    if selectedAuthors:
        data1 = data1.filter(author__in=selectedAuthors)

    if selectedLanguages:
        print(selectedLanguages)
        data1 = data1.filter(language__in=selectedLanguages)

    
    page = request.GET.get('page', 1)
    paginator = Paginator(data1, 16)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    if is_ajax_request:
        print(data1)
        # If it's an AJAX request, return a JSON response
        response_data = {
            'products': serialize_products(data, request),
            'min': min_price,
            'max': max_price,
        }
        return JsonResponse(response_data)
    else:
        
        return render(request, 'store/product_page.html', {'products': data, 'min': min_price, 'max': max_price, 'authors':authors})



def product_detail(request, slug):

    product = get_object_or_404(Product, slug=slug, is_active=True)
    specifications = ProductSpecifiactionValue.objects.filter(product=product)
    allcomments = product.comments.filter(status=True)
    average_rating = Review.objects.filter(
        post=product).aggregate(Avg("rate"))["rate__avg"] or 0
    comment_form = NewCommentForm()

    top_comment = Review.objects.filter(rate=5, post=product).last()

    if request.user.is_authenticated:
        user_name = request.user.name
    else:
        user_name = "user"
        
    
    if allcomments.count() == 0:
        five_avg_rating = 0.00
        four_avg_rating = 0.00
        three_avg_rating = 0.00
        two_avg_rating = 0.00
        avg_rating = 0.00
    else:
        five_avg_rating = Review.objects.filter(
            rate=5, post=product).count()
        five_avg_rating = (five_avg_rating / allcomments.count()) * \
            100 if five_avg_rating != None else 0.0

        four_avg_rating = Review.objects.filter(
            rate=4, post=product).count()
        four_avg_rating = (four_avg_rating / allcomments.count()) * \
            100 if four_avg_rating != None else 0.0

        three_avg_rating = Review.objects.filter(
            rate=3, post=product).count()
        three_avg_rating = (three_avg_rating / allcomments.count()) * \
            100 if three_avg_rating != None else 0.0

        two_avg_rating = Review.objects.filter(
            rate=2, post=product).count()
        two_avg_rating = (two_avg_rating / allcomments.count()) * \
            100 if two_avg_rating != None else 0.0

        avg_rating = Review.objects.filter(
            rate=1, post=product).count()
        avg_rating = (avg_rating / allcomments.count()) * \
            100 if avg_rating != None else 0.0

    similar_products = Product.objects.filter(category=product.category).exclude(id=product.id).order_by('?')[:4]
    different_products = Product.objects.exclude(category=product.category).order_by('?')[:4]
    
    return render(request, 'store/detail1.html', {'product': product, 'comments': allcomments, 'comment_form': comment_form,
                                                      'user_name': user_name, 'allcomments': allcomments, 'average_rating': average_rating,
                                                      'five_avg_rating': five_avg_rating, 'four_avg_rating': four_avg_rating, 'three_avg_rating': three_avg_rating, 'two_avg_rating': two_avg_rating, 'avg_rating': avg_rating,
                                                      'top_comment': top_comment,'similar_products': similar_products,'specifications': specifications, 'different_products':different_products})


@login_required
def addcomment(request):

    user = request.user
    user_email = request.user.email
    user_comment = None
    image = get_object_or_404(Profile, user=user)

    if request.method == 'POST':

        if request.POST.get('action') == 'delete':
            id = request.POST.get('nodeid')
            print(id)
            c = Review.objects.get(id=id)
            c.delete()
            return JsonResponse({'remove': id})
        else:
            comment_form = NewCommentForm(request.POST)
            print(comment_form)
            if comment_form.is_valid():
                user_comment = comment_form.save(commit=False)
                user_comment.name = request.user
                user_comment.email = user_email
                user_comment.image = image
                user_comment.save()
                user_name = request.user.name
                result = comment_form.cleaned_data.get('content')
                return JsonResponse({'result': result, 'user_name': user_name})


