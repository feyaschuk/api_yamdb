# Generated by Django 2.2.16 on 2021-08-18 17:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reviews", "0003_auto_20210818_2159"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(
                help_text="Укажите название категории",
                max_length=200,
                verbose_name="Название категории",
            ),
        ),
        migrations.AlterField(
            model_name="genre",
            name="name",
            field=models.CharField(
                help_text="Укажите жанр",
                max_length=200,
                verbose_name="Название жанра",
            ),
        ),
        migrations.AlterField(
            model_name="title",
            name="name",
            field=models.CharField(
                max_length=200, verbose_name="Название произведения"
            ),
        ),
        migrations.AlterField(
            model_name="title",
            name="year",
            field=models.PositiveSmallIntegerField(
                validators=[
                    django.core.validators.MaxValueValidator(
                        2021, "Год не может быть больше текущего"
                    )
                ],
                verbose_name="Год выпуска",
            ),
        ),
    ]
