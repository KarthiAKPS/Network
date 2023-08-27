# Generated by Django 4.2.4 on 2023-08-27 10:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('creater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='name', to=settings.AUTH_USER_MODEL)),
                ('liked', models.ManyToManyField(blank=True, null=True, related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
