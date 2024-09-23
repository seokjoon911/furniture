from django.db import models
from product.models import Product
from django.conf import settings
import uuid

class Inquiry(models.Model):
    inq_id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    prod_id = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='prod_id', related_name='prod_inq')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='user', to_field='nickname')
    title = models.CharField(max_length=100)
    contents = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # 생성시 자동으로 시간저장
    is_public = models.BooleanField(default=True) # 공개/비공개

    class Meta:
        db_table = 'inquiry'