# Generated by Django 2.2.1 on 2019-06-05 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0005_delete_employeename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='hire_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
