from django.db import models

# Create your models here.

from django.db import models

class Interval(models.Model):
    name = models.CharField(max_length=200, db_index=True, unique=True)
    symbol = models.CharField(max_length=200, db_index=True, unique=True)
    pub_date = models.DateTimeField('date published')

class PriceType(models.Model):
    name = models.CharField(max_length=200, db_index=True, unique=True)
    pub_date = models.DateTimeField('date published')

class Instrument(models.Model):
    name = models.CharField(max_length=200, db_index=True, unique=True)
    us_margin_requirement = models.FloatField()
    pub_date = models.DateTimeField('date published')

class Timestamp(models.Model):
    timestamp = models.BigIntegerField(db_index=True)
    pub_date = models.DateTimeField('date published')

class Volume(models.Model):
    volume = models.IntegerField(db_index=True)
    pub_date = models.DateTimeField('date published')
    
class Candlestick(models.Model):
    o = models.FloatField()
    l = models.FloatField()
    h = models.FloatField()
    c = models.FloatField()
    volume = models.ForeignKey(Volume, on_delete=models.CASCADE, db_index=True)
    timestamp = models.ForeignKey(Timestamp, on_delete=models.CASCADE, db_index=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, db_index=True)
    price_type = models.ForeignKey(PriceType, on_delete=models.CASCADE, db_index=True)
    interval = models.ForeignKey(Interval, on_delete=models.CASCADE, db_index=True)
    pub_date = models.DateTimeField('date published')

    class Meta:
        index_together = [
            ('timestamp', 'instrument', 'price_type', 'interval'),
            ]
        unique_together = [
            ('timestamp', 'instrument', 'price_type', 'interval'),
        ]
