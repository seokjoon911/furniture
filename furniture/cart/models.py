from django.db import models
import uuid
from django.conf import settings

class Cart(models.Model):
    cart_id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='user', to_field='nickname')
    prod_id = models.ForeignKey('product.Product', on_delete=models.CASCADE, db_column='prod_id', to_field='prod_id')
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart'