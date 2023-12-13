from .models import Order , OrderItem

def Orders(request):
    return {'Orders':Order(request)}

def Orderitems(request):
    return {'Orderitems':OrderItem(request)}