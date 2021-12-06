# Generated by Django 3.2.9 on 2021-12-06 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion1', '0007_alter_productos_vendedor'),
    ]

    operations = [
        migrations.CreateModel(
            name='mensajes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comprador', models.CharField(max_length=20)),
                ('msg', models.CharField(max_length=350)),
                ('rate', models.CharField(max_length=1)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aplicacion1.productos')),
            ],
            options={
                'verbose_name': 'mensaje',
                'verbose_name_plural': 'mensajes',
                'db_table': 'mensaje',
                'ordering': ['id'],
            },
        ),
    ]
