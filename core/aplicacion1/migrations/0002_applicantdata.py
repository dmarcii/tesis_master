# Generated by Django 3.2.9 on 2021-11-27 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicantData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheduled_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
