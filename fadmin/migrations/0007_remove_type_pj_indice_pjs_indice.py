# Generated by Django 4.2.8 on 2023-12-06 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fadmin', '0006_rename_p_pjs_name_rename_pj_type_pj_name_pj_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='type_pj',
            name='indice',
        ),
        migrations.AddField(
            model_name='pjs',
            name='indice',
            field=models.CharField(default=1, max_length=3),
            preserve_default=False,
        ),
    ]