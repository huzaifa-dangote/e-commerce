# Generated by Django 5.0.6 on 2024-06-22 07:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_remove_user_watchlist_listing_watchlist_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='bid',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bid_listing', to='auctions.bid'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='comment',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_listing', to='auctions.comment'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posted_listings', to=settings.AUTH_USER_MODEL),
        ),
    ]
