from django.db import models
from account.models import Customer, Profile

# Create your models here.
from django.db import models
from django.utils import timezone
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _
from django.db.models import Avg
from mptt.managers import TreeManager
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

def user_directory_path(instance, filename):
    return 'posts/images/{0}/{1}'.format(instance.id, filename)


class Post(models.Model):

    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, default=1)
    title = models.CharField(max_length=250)
    excerpt = models.TextField(null=True)
    image = models.ImageField(
        upload_to=user_directory_path, default='posts/default.jpg')
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    publish = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    status = models.CharField(max_length=10, choices=options, default='draft')
    objects = models.Manager()  # default manager
    newmanager = NewManager()  # custom manager

    def get_absolute_url(self):
        return reverse('blog:post_single', args=[self.slug])

    def average_rating(self) -> float:
        return Comment.objects.filter(post=self).aggregate(Avg("rate"))["rate__avg"] or 0
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


RATE_CHOICES = [

    (0 ,'its a comment'),
    (1, '1-Trash'),
    (2, '2-Horrible'),
    (3, '3-Average'),
    (4, '4-Nice'),
    (5, '5-Very Good'),

]


class Comment(MPTTModel):

    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.ForeignKey(Customer, verbose_name=_(
        "Customer"), on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', db_index=True)
    email = models.EmailField()
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES)
    image = models.ForeignKey(
        Profile, related_name='image', on_delete=models.CASCADE)

    objects = TreeManager()
    class MPTTMeta:
        order_insertion_by = ['publish']
        

    def __str__(self):
        return str(self.name)



