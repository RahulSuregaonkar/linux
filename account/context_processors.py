from .models import Address

def address(request):
    if request.user.is_authenticated:
        user_name = request.user
    else:
        user_name = None
            
    return {
        'addresses': Address.objects.filter(customer=user_name)
    }