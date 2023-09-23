# Generated by Django 4.2.5 on 2023-09-22 15:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lunches', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lunch',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_lunches', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lunch',
            name='sender_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_lunches', to=settings.AUTH_USER_MODEL),
        ),
    ]
