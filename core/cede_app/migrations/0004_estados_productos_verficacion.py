# Generated by Django 3.2.9 on 2021-12-11 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cede_app', '0003_estados_productos'),
    ]

    operations = [
        migrations.AddField(
            model_name='estados_productos',
            name='verficacion',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
