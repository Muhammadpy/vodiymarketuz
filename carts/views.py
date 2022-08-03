from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product ,Variation
from . models import Cart
from . models import CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


#Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request, product_id):
    current_user=request.user
    product = Product.objects.get(id = product_id) #get the product
    # if user is authenticated
    if current_user.is_authenticated:
        pass
    else:

        product_variation=[]
        if request.method == "POST":
            for item in request.POST:
                print(item)
                key=item
                value=request.POST[key]
                print(key, value)
                try:
                    variation=Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    print(variation)
                    product_variation.append(variation)
                except:
                    pass



        try:
            cart=Cart.objects.get(card_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart=Cart.objects.create( card_id=_cart_id(request))
            cart.save()

                    
        is_cart_item_exists=CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item=CartItem.objects.filter(product=product,cart=cart)    

        #color=request.GET['color']
        # size=request.GET['size']
        # return HttpResponse (color)
        # exit()
            ex_var_list =[]
            id= []
            for item in cart_item:
                existing_variation = item.variation.all()
                ex_var_list.append(list(existing_variation)) 
                id.append(item.id)
            print(ex_var_list)
    
            if product_variation in ex_var_list:
                #increase the cart item quantity
                index=ex_var_list.index(product_variation)
                item_id=id[index]
                item=CartItem.objects.get(product=product, id=item_id)
                item.quantity+=1
                item.save()
                
        

            else:
                item=CartItem.objects.create(product=product, quantity =1, cart=cart)
                if  len(product_variation)>0:
                    item.variation.clear()
                    item.variation.add(
                        
                    )
                
                item.save()
        else:
            cart_item=CartItem.objects.create(
                product=product, 
                quantity=1, 
                cart = cart,
            )

            if  len(product_variation)>0:     
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
            cart_item.save()
        return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    cart=Cart.objects.get(card_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
   
    try:
        cart_item=CartItem.objects.get(product=product, cart=cart, id = cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -=1 
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id ):
    cart=Cart.objects.get(card_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item= CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')






def cart(request, total=0, quantity=0, carts_items=None  ):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            carts_items=CartItem.objects.filter(user=request.user,  is_active=True)
            print(carts_items, 'cart ')
        else:

            cart= Cart.objects.get(card_id=_cart_id(request))
            carts_items=CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in carts_items:
            print("OK shu yerdda")
            print(carts_items)
            total += cart_item.product.Price
            
            quantity+=cart_item.quantity
            total = quantity *cart_item.product.Price
        tax= (2*total)/100
        grand_total=total + tax
        
    except :ObjectDoesNotExist
        
        
    
        

    context ={
        'total':total,
        'quantity': quantity,
        'carts_items':carts_items,
        'tax' : tax,   
        'grand_total':grand_total,
        
    }
    return render (request, 'store/cart.html', context)
    


@login_required( login_url = 'accounts:login')
def checkout(request, total=0, quantity=0, carts_items=None):
    try:
        tax=0
        grand_total=0
        cart= Cart.objects.get(card_id=_cart_id(request))
        carts_items=CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in carts_items:
            print("OK")
            total += cart_item.product.Price
            
            quantity+=cart_item.quantity
            total = quantity *cart_item.product.Price
        tax= (2*total)/100
        grand_total=total + tax
        
    except :ObjectDoesNotExist

    context ={
        'total':total,
        'quantity': quantity,
        'carts_items':carts_items,
        'tax' : tax,   
        'grand_total':grand_total,
        
    }
    return render(request, 'store/checkout.html', context)