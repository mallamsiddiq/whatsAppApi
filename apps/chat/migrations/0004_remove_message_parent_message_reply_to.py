# Generated by Django 5.0 on 2023-12-09 07:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_message_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='parent',
        ),
        migrations.AddField(
            model_name='message',
            name='reply_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='chat.message'),
        ),
    ]
