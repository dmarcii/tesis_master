# Generated by Django 3.2.9 on 2021-12-01 23:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aplicacion1', '0005_perfil_datos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='vendedor',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
