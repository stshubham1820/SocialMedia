# Generated by Django 3.2.9 on 2022-01-30 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alluser', '0002_alter_user_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.CharField(max_length=14, unique=True),
        ),
    ]