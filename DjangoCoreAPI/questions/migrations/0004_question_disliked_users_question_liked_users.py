# Generated by Django 4.2.16 on 2024-11-23 21:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0003_rename_dislike_users_comment_disliked_users_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='disliked_users',
            field=models.ManyToManyField(blank=True, related_name='disliked_questions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='liked_users',
            field=models.ManyToManyField(blank=True, related_name='liked_questions', to=settings.AUTH_USER_MODEL),
        ),
    ]
