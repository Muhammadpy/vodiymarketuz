from django.db import models
from numpy import product
from store.models import Product, Variation



from store.models import Product

# Create your models here.
class Cart(models.Model):
    card_id  = models.CharField(max_length=100, blank=True)
    date_add = models.DateField(auto_now_add=True)


    def __str__(self) -> str:
        return self.card_id

class CartItem(models.Model):
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation =models.ManyToManyField(Variation, blank=True)
    cart     =models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity =models.IntegerField()
    is_active=models.BooleanField(default=True)
    

    def sub_total(self):
        return self.product.Price * self.quantity

    def __unicode__(self) :
        return self.product