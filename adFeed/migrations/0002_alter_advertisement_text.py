# Generated by Django 4.2.4 on 2023-08-11 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adFeed', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='text',
            field=models.TextField(),
        ),
    ]
