from django.db import models
# Create your models here.

class Fadmin(models.Model):
    id = models.AutoField(primary_key=True)
    date_arr = models.DateField(auto_now_add=True, verbose_name="تاريخ التوصل")
    num_env = models.CharField(max_length=20, verbose_name="رقم الارسال")
    num_rapp_pj = models.CharField(max_length=20, verbose_name="رقم محضر الضابطة القضائية")
    pj = models.CharField(max_length=30, verbose_name="الضابطة القضائية")
    num_rapp_pp = models.CharField(max_length=20 , verbose_name="رقم محضر النيابة العامة")
    num_plaint = models.CharField(max_length=20, verbose_name="رقم الشكاية")
    note = models.CharField(max_length=100, verbose_name="ملاحظات" , blank=True , null=True)
    search_indice = models.IntegerField(verbose_name="عدد مرات البحث", blank=True , null=True)

    def __str__(self):
        return self.pj
