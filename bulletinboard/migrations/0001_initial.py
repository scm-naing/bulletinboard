# Generated by Django 4.0.1 on 2022-01-21 08:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('password', models.CharField(max_length=255)),
                ('profile', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('0', 'Admin'), ('1', 'User')], default='1', max_length=1)),
                ('phone', models.CharField(max_length=20, null=True)),
                ('address', models.CharField(max_length=255, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('created_user_id', models.IntegerField(default=1)),
                ('updated_user_id', models.IntegerField(default=1)),
                ('delete_user_id', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('0', 'inactive'), ('1', 'active')], default='1', max_length=1)),
                ('created_user_id', models.IntegerField()),
                ('updated_user_id', models.IntegerField()),
                ('delete_user_id', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
    ]