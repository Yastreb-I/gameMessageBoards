# Generated by Django 4.2.4 on 2023-08-11 14:51

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('adFeed', '0002_alter_advertisement_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='text',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Text'),
        ),
    ]
