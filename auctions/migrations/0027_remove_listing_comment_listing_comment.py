# Generated by Django 5.0.6 on 2024-06-28 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0026_alter_listing_comment_alter_listing_winner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='comment',
        ),
        migrations.AddField(
            model_name='listing',
            name='comment',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='comment_listing', to='auctions.comment'),
        ),
    ]