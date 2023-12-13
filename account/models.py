import uuid

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.dispatch import receiver
from django.db.models.signals import post_save
from store.models import Product
from django.db.models import Avg
from mptt.models import MPTTModel, TreeForeignKey


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, name, password, **other_fields)

    def create_user(self, email, name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, name=name,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user

def user_directory_path(instance, filename):
    return 'users/avatars/{0}/{1}'.format(instance.user.id, filename)

class Customer(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=150, unique=True)
    mobile = models.CharField(max_length=12, blank=True)
    # Delivery details
    country = CountryField()
    # User Status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(
        upload_to=user_directory_path, default='images/rahul_pic_.jpeg'
    )

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'l@1.com',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.name





class Profile(models.Model):
    user = models.OneToOneField(Customer, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to=user_directory_path, default='images/rahul_pic_.jpeg'
    )
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.name


@ receiver(post_save, sender=Customer)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Address(models.Model):
    """ADDress

    Args:
        models (_type_): customer to add address
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, verbose_name=_(
        "Customer"), on_delete=models.CASCADE)
    full_name = models.CharField(_("Full Name"), max_length=150)
    phone = models.CharField(_("Phone Number"), max_length=50)
    postcode = models.CharField(_("Post code"), max_length=50)
    address_line = models.CharField(_("Address Line 1"), max_length=250)
    address_line2 = models.CharField(_("Address Line 2"), max_length=255)
    town_city = models.CharField(_("Town/city/State"), max_length=150)
    delivery_instructions = models.CharField(
        _("Delivery Instructions"), max_length=250)
    updated_at = models.DateTimeField(_("Created at"), auto_now=True)
    created_at = models.DateTimeField(_("updated at"), auto_now_add=True)
    default = models.BooleanField(_("Default"), default=False)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Adresses"

    def __str__(self):
        return self.customer.name


RATE_CHOICES = [
    
    (0 ,'its a comment'),
    (1,'1-Trash'),
    (2,'2-Horrible'),
    (3,'3-Average'),
    (4,'4-Nice'),
    (5, '5-Very Good'),    
    
]

class Review(MPTTModel):

    post = models.ForeignKey(Product,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.ForeignKey(Customer, verbose_name=_("Customer"), on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    email = models.EmailField()
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, blank= False)
    image = models.ForeignKey(Profile, related_name='images', on_delete=models.CASCADE)
    
    class MPTTMeta:
        order_insertion_by = ['publish']
              
    def __str__(self):
        return str(self.name)
    