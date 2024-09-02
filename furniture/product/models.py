from django.db import models
import uuid
from django.conf import settings

class Product(models.Model):
    prod_id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField() #글 내용
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='user', to_field='nickname')
    image = models.ImageField(null=True)  # 피드 이미지
    price = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product'