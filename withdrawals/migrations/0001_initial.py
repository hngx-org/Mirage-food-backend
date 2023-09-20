# Generated by Django 4.2.5 on 2023-09-19 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Withdrawal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=200, verbose_name='user ID')),
                ('status', models.CharField(choices=[('pending', 'processing'), ('completed', 'done')], max_length=20, verbose_name='withdrawal status')),
                ('amount', models.BigIntegerField(verbose_name='withdrawal amount')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='withdrawal timestamp')),
            ],
        ),
    ]
