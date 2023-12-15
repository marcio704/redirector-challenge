# Generated by Django 4.2.8 on 2023-12-15 00:16

from django.db import migrations, models
import django.db.models.deletion
import redirector.behaviors


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DomainPool",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, unique=True)),
                ("description", models.TextField()),
            ],
            bases=(redirector.behaviors.Timestampable, models.Model),
        ),
        migrations.CreateModel(
            name="Domain",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.URLField(unique=True)),
                ("weight", models.SmallIntegerField()),
                (
                    "domain_pool",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="domains",
                        to="redirector.domainpool",
                    ),
                ),
            ],
            bases=(redirector.behaviors.Timestampable, models.Model),
        ),
    ]