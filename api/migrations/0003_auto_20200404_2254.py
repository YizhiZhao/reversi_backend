# Generated by Django 3.0.4 on 2020-04-04 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_userhistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useracl',
            name='id',
        ),
        migrations.AlterField(
            model_name='useracl',
            name='name',
            field=models.CharField(max_length=200, primary_key=True, serialize=False, unique=True),
        ),
    ]