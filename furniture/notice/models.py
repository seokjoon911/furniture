from django.conf import settings
from django.db import models


class Notice(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='user',to_field='nickname')
    title = models.CharField(max_length=50) # 제목
    content = models.TextField() # 내용
    created_at = models.DateTimeField(auto_now_add=True) # 생성시 자동으로 시간저장
    updated_at = models.DateTimeField(auto_now=True) # 수정시 자동으로 시간저장
    is_public = models.BooleanField(default=True) # 공개/비공개

    class Meta:
        db_table = 'notice'
        ordering = ['-id']