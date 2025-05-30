# Generated by Django 4.2.20 on 2025-05-21 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("ads", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExchangeProposal",
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
                (
                    "comment",
                    models.TextField(
                        blank=True,
                        null=True,
                        verbose_name="Комментарий к предложению",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "В ожидании"),
                            ("accepted", "Принято"),
                            ("rejected", "Отклонено"),
                        ],
                        default="pending",
                        max_length=10,
                        verbose_name="Статус предложения обмена",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="Дата предложения обмена",
                    ),
                ),
                (
                    "ad_receiver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exchange_proposals_received",
                        to="ads.ad",
                        verbose_name="Объявление получателя",
                    ),
                ),
                (
                    "ad_sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exchange_proposals_sent",
                        to="ads.ad",
                        verbose_name="Объявление отправителя",
                    ),
                ),
            ],
            options={
                "verbose_name": "Предложение обмена",
                "verbose_name_plural": "Предложения обмена",
                "ordering": ("-created_at",),
                "indexes": [
                    models.Index(fields=["ad_sender"], name="ad_sender_idx"),
                    models.Index(
                        fields=["ad_receiver"], name="ad_receiver_idx"
                    ),
                ],
            },
        ),
        migrations.AddConstraint(
            model_name="exchangeproposal",
            constraint=models.UniqueConstraint(
                fields=("ad_sender", "ad_receiver"),
                name="unique_exchange_proposal",
                violation_error_message="Предложение обмена уже существует для этих объявлений.",
            ),
        ),
    ]
