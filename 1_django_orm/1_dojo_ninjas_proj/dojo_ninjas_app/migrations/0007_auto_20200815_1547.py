# Generated by Django 2.2.4 on 2020-08-15 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojo_ninjas_app', '0006_auto_20200815_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dojos',
            name='desc',
            field=models.TextField(verbose_name='old dojo'),
        ),
    ]