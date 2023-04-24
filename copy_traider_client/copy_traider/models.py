from statistics import mode
from django.db import models
from django.urls import reverse

# Create your models here.


class Symbols(models.Model):

    # Fields
    name = models.CharField(max_length=255)
    # slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    amount = models.DecimalField(max_digits=20, decimal_places=10, default=0)
    last_price = models.DecimalField(
        max_digits=20, decimal_places=10, default=0)
    last_price_update = models.DateTimeField(null=True, blank=True)
    broker = models.CharField(max_length=30)
    monitor = models.BooleanField(default=False)
    presision = models.IntegerField(null=True, blank=True)
    scale = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
    # class Meta:
    #     ordering = ('-created',)

    # def __unicode__(self):
    #     return u'%s' % self.slug

    # def get_absolute_url(self):
    #     return reverse('trade_symbols_detail', args=(self.slug,))

    # def get_update_url(self):
    #     return reverse('trade_symbols_update', args=(self.slug,))


class OpenOrders(models.Model):
    symbol = models.ForeignKey(
        Symbols,
        on_delete=models.CASCADE, related_name="OpenOrder"
    )
    ticket = models.IntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    tp = models.FloatField(null=True, blank=True)
    sl = models.FloatField(null=True, blank=True)
    volume = models.FloatField(null=True, blank=True)
    type = models.CharField(max_length=600, blank=True, null=True)
    active = models.BooleanField(default=True)
    return_object = models.CharField(max_length=600, blank=True, null=True)


class OpenPositions(models.Model):
    symbol = models.ForeignKey(
        Symbols,
        on_delete=models.CASCADE, related_name="Openposition"
    )
    ticket = models.IntegerField(null=True, blank=True)
    side = models.CharField(max_length=100, blank=True, null=True)
    open_price = models.FloatField(null=True, blank=True)
    volume = models.FloatField(null=True, blank=True)
    active = models.BooleanField(default=False)
    tp = models.FloatField(null=True, blank=True)
    sl = models.FloatField(null=True, blank=True)
    # set_second = models.BooleanField(default=False)

    def __str__(self):
        return str(self.ticket)
