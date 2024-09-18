from django.db import models

class Category(models.Model): #카테고리(가구)
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'categories'

class SubCategory(models.Model): #하위 카테고리(침대,소파 등등)
    name = models.CharField(max_length=30)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_categories'