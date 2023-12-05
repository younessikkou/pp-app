from django.db import models
# Create your models here.

class Fadmin(models.Model):
    id = models.AutoField(primary_key=True)
    date_arr = models.DateField(auto_now_add=True)
    num_env = models.CharField(max_length=10)
    num_rapp_pj = models.CharField(max_length=10)
    pj = models.CharField(max_length=20)
    num_rapp_pp = models.CharField(max_length=10)
    num_plaint = models.CharField(max_length=10)
    note = models.CharField(max_length=100)
    search_indice = models.IntegerField()

    def __str__(self):
        return self.pj
