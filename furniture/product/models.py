from django.db import models
import uuid
from django.conf import settings
from menu.models import SubCategory
from urllib.parse import urlparse, unquote

class Product(models.Model):
    prod_id = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='user', to_field='nickname')
    category_id = models.ForeignKey(SubCategory, on_delete=models.CASCADE, db_column='category_id', to_field='id')
    title = models.CharField(max_length=100)  # 제목
    content = models.TextField()  # 내용
    url = models.ImageField(null=True)  # 피드 이미지
    price = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True) #제품 공개/비공개

    class Meta:
        db_table = 'product'

    @property
    def file_url(self):
        parsed_url = urlparse(self.url.url)
        decoded_path = unquote(parsed_url.path)
        if decoded_path.startswith('/'):
            decoded_path = decoded_path[1:]
        return decoded_path