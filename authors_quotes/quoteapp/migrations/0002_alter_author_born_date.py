# Generated by Django 5.0.1 on 2024-02-05 18:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quoteapp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="author",
            name="born_date",
            field=models.DateField(),
        ),
    ]
