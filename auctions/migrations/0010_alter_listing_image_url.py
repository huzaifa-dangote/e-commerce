# Generated by Django 5.0.6 on 2024-06-19 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_bid_user_alter_comment_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image_url',
            field=models.URLField(blank=True, default=None, null=True),
        ),
    ]