# Generated by Django 5.1.4 on 2025-01-05 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0002_order_order_status_alter_order_order_key"),
    ]

    operations = [
        migrations.RemoveField(model_name="order", name="billing_status",),
    ]