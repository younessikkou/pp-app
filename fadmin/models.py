from django.db import models
# Create your models here.


class Type_pj(models.Model):
    name_pj = models.CharField(max_length=30)

    def __str__(self):
        return self.name_pj


class Pjs(models.Model):
    indice = models.CharField(max_length=3)
    name = models.CharField(max_length=100,unique=True)
    reporter = models.ForeignKey(Type_pj, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Type_rapp(models.Model):
    indice = models.CharField(max_length=20, verbose_name="رمز المحضر", blank=False , null=False,unique=True)
    nom_typerapp = models.CharField(max_length=20, verbose_name="رمز المحضر", blank=False , null=False)

    def __str__(self):
        return self.nom_typerapp



class Fadmin(models.Model):
    date_arr = models.DateField(auto_now_add=True, verbose_name="تاريخ التوصل")
    num_env = models.CharField(max_length=20, verbose_name="رقم الارسال", blank=True , null=True)
    num_rapp_pj = models.CharField(max_length=20, verbose_name="رقم محضر الضابطة القضائية", blank=True , null=True)
    num_rapp_pp = models.CharField(max_length=20 , verbose_name="رقم محضر النيابة العامة", blank=True , null=True)
    num_plaint = models.CharField(max_length=20, verbose_name="رقم الشكاية", blank=True , null=True)
    note = models.CharField(max_length=100, verbose_name="ملاحظات" , blank=True , null=True)
    search_indice = models.IntegerField(verbose_name="عدد مرات البحث", blank=True , null=True)
    type_pj = models.ForeignKey(Pjs, on_delete=models.CASCADE,related_name="fadmins",verbose_name="الضابطة القضائية")
    type_rapp = models.ForeignKey(Type_rapp, on_delete=models.CASCADE,related_name="rapp_type",verbose_name="نوع المحضر")

    def __str__(self):
        return self.num_env

