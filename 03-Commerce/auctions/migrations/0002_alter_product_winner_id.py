# Generated by Django 4.1 on 2022-09-02 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='winner_id',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]