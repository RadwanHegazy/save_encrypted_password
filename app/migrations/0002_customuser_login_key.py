# Generated by Django 4.0 on 2023-02-24 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='login_key',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
    ]
