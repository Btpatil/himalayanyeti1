# Generated by Django 4.1.4 on 2022-12-25 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_label_parentcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
