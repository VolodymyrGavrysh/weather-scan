# Generated by Django 2.2.10 on 2020-02-29 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('endpoints', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mlrequest',
            name='feedback',
            field=models.CharField(blank=True, max_length=9000, null=True),
        ),
    ]
