from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from djmoney.models.fields import MoneyField
from bananas.models import UUIDModel, TimeStampedModel
from moneyed import Money


class Account(UUIDModel, TimeStampedModel):
    user = models.ForeignKey(User, null=True, blank=True)

    # The card id is a uid from a mifare classic 1k card and is supposed
    # to be 8 bytes long.
    card_id = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.id)


class Purchase(UUIDModel, TimeStampedModel):
    account = models.ForeignKey(Account)

    @property
    def amount(self):
        amount = self.items.aggregate(amount=models.Sum('amount'))['amount']
        return Money(amount or 0, settings.DEFAULT_CURRENCY)

    def __str__(self):
        return str(self.id)


class PurchaseItem(UUIDModel):
    purchase = models.ForeignKey(Purchase, related_name='items')
    product_id = models.UUIDField()
    qty = models.IntegerField(default=0)
    amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency=settings.DEFAULT_CURRENCY
    )

    def __str__(self):
        return str(self.id)
