import json
from .models import *

def cookieCart(request):
    try:
         cart = json.loads(request.COOKIES['cart'])
    except:
         cart = {} #if empty, create one

    print('Cart:', cart)	
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            product = Product.objects.get(id = i)
            total = (product.price*cart[i]['quantity'])
                
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
            # build item object that can be queried in the html
            item = {
                    'product': {
                        'id':product.id,
                        'name': product.name,
                        'price':product.price,
                        'imageURL':product.imageURL,
                          },
                    'quantity': cart[i]['quantity'],
                    'get_total': total
                    }
            items.append(item)

            if product.digital ==False:
                order['shipping'] = True
        except:
            pass
    return {'cartItems':cartItems, 'order':order, 'items':items}


def carData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:# for unauthenticated users: item, cart total will be 0, so the rest page content still shows
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems':cartItems, 'order':order, 'items':items}