# Generated by Django 2.2.4 on 2020-08-15 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojo_ninjas_app', '0004_auto_20200815_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='dojos',
            name='desc',
            field=models.TextField(default=2),
            preserve_default=False,
        ),
    ]