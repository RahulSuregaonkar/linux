from django.shortcuts import redirect, render, get_object_or_404, HttpResponseRedirect
from .models import Post, Comment, Category
from .forms import NewCommentForm
from django.db.models import Q
from account.models import Profile
from mptt.templatetags.mptt_tags import get_cached_trees, cache_tree_children
from django.contrib.postgres.search import SearchVector

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
# Create your views here.
from django.views.generic import ListView


def home(request):

    all_posts = Post.newmanager.filter(category_id=8)
    quick_read = Post.newmanager.filter(category_id=10)
    science = Post.newmanager.filter(category_id=9)
    tech = Post.newmanager.filter(category_id=1).first()
    travel = Post.newmanager.filter(category_id=3).first()
    health = Post.newmanager.filter(category_id=11).first()

    return render(request, 'blog/index.html', {'posts': all_posts, 'quick_read': quick_read, "science_posts": science, "technologies": tech, "travel": travel, "health": health})


def all_blog(request):
    all_blog = Post.newmanager.all()

    return render(request, 'blog/all_post.html', {'posts': all_blog})


def post_single(request, post):
    post = get_object_or_404(Post, slug=post, status='published')
    all_comments = list(post.comments.filter(status=True))

    comment_form = NewCommentForm()

    total_comments = len(all_comments)

    return render(
        request,
        'blog/post.html',
        {
            'post': post,
            'comment_form': comment_form,
            'comments': all_comments,
            'user_name': request.user.name if request.user.is_authenticated else "user",
            'allcomments': total_comments,
        }
    )


class CatListView(ListView):
    template_name = 'blog/category.html'
    context_object_name = 'catlist'

    def get_queryset(self):
        content = {
            'cat': self.kwargs['category'],
            'posts': Post.objects.filter(category__name=self.kwargs['category']).filter(status='published')
        }
        return content


def category_list(request):
    category_list = Category.objects.exclude(name='default')
    context = {
        "category_list": category_list,
    }
    return context


def post_search(request):

    data = []  # Initialize data with an empty list or default value

    if 'q' in request.GET:
        q = request.GET['q']
        data = Post.objects.annotate(
            search=SearchVector('title', 'slug')
        ).filter(search=q)

    if request.method == 'POST' and 'q' in request.POST:
        q = request.POST['q']
        data = Post.objects.filter(title__icontains=q, slug__icontains=q)[
            :10]  # Limit the results to 10
        # Extract relevant information for suggestions (customize based on your Product model)
        suggestions = [{'id': product.slug, 'title': product.title,
                        } for product in data]
        return JsonResponse({'suggestions': suggestions})

    return render(request, 'blog/search.html', {
        'q': q,
        'results': data})


def addcomment(request):
    user = request.user
    user_email = request.user.email
    user_comment = None
    image = get_object_or_404(Profile, user=user)

    if request.method == 'POST':

        if request.POST.get('action') == 'delete':
            id = request.POST.get('nodeid')
            print(id)
            c = Comment.objects.get(id=id)
            c.delete()
            return JsonResponse({'remove': id})
        else:
            comment_form = NewCommentForm(request.POST)
            if comment_form.is_valid():
                user_comment = comment_form.save(commit=False)
                user_comment.name = request.user
                user_comment.email = user_email
                user_comment.image = image
                user_comment.save()
                user_name = request.user.name
                result = comment_form.cleaned_data.get('content')
                return JsonResponse({'result': result, 'user_name': user_name})
