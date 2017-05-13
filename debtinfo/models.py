from django.db import models
from django.conf import settings
from decimal import Decimal
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save


class CurrencyField(models.DecimalField):
    """Format value into currency format.

    Inherits from models.DecimalField.
    """

    def __init__(self, *args, **kwargs):
        kwargs['max_digits'] = 11
        kwargs['decimal_places'] = 2
        super(CurrencyField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        try:
            return super(CurrencyField, self).to_python(value).quantize(Decimal('0.01'))
        except AttributeError:
            return None


class Profile(models.Model):
    """A database model of debt information."""

    debtor = models.ForeignKey(settings.AUTH_USER_MODEL, null=False,
                               on_delete=models.CASCADE, related_name='profile_debtor')
    creditor = models.ForeignKey(settings.AUTH_USER_MODEL, null=False,
                                 on_delete=models.CASCADE, related_name='profile_creditor')
    id_number = models.CharField(max_length=10, null=False)
    cell = models.CharField(max_length=12, null=False)
    amount = CurrencyField()

    class Meta:
        db_table = 'tb_profiles'

    def __str__(self):
        return self.debtor.username


class Debtor(models.Model):
    """A database model of a Debtor."""

    debtor = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE, related_name='debtor')
    id_number = models.CharField(max_length=10, blank=False)
    cell = models.CharField(max_length=12, blank=False)

    class Meta:
        db_table = 'tbl_due_listing'

    def __str__(self):
        return self.debtor.username


@receiver(post_save, sender=Profile)
def add_debtor(sender, **kwargs):
    """Create a Debtor instance for a created Profile instance."""
    profile = kwargs['instance']

    if kwargs['created']:
        try:
            debtor = Debtor.objects.get(debtor=profile.debtor)
        except Debtor.DoesNotExist:
            debtor = Debtor.objects.create(
                debtor=profile.debtor, id_number=profile.id_number, cell=profile.cell)
        else:
            pass
