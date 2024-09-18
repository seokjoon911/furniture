from django.db import models
import uuid
from django.conf import settings
from menu.models import SubCategory

class Product(models.Model):
    prod_id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100) #제목
    content = models.TextField() #내용
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='user', to_field='nickname')
#    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, db_column='id', to_field='id')
    image = models.ImageField(null=True)  # 피드 이미지
    price = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True) #제품 공개/비공개

    class Meta:
        db_table = 'product'