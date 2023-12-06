from django.db import models
# Create your models here.


class Type_pj(models.Model):
    name_pj = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name_pj}"


class Pjs(models.Model):
    indice = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    reporter = models.ForeignKey(Type_pj, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

class Fadmin(models.Model):
    date_arr = models.DateField(auto_now_add=True, verbose_name="تاريخ التوصل")
    num_env = models.CharField(max_length=20, verbose_name="رقم الارسال")
    num_rapp_pj = models.CharField(max_length=20, verbose_name="رقم محضر الضابطة القضائية")
    num_rapp_pp = models.CharField(max_length=20 , verbose_name="رقم محضر النيابة العامة")
    num_plaint = models.CharField(max_length=20, verbose_name="رقم الشكاية")
    note = models.CharField(max_length=100, verbose_name="ملاحظات" , blank=True , null=True)
    search_indice = models.IntegerField(verbose_name="عدد مرات البحث", blank=True , null=True)
    pj = models.OneToOneField(Pjs,on_delete=models.CASCADE,primary_key=True,verbose_name="الضابطة القضائية")


    def __str__(self):
        return self.num_env
