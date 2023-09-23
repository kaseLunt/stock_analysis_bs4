from django.db import models
from django.utils import timezone

class StockData(models.Model):
    # Automatically add an ID field
    id = models.AutoField(primary_key=True)
    
    # Add a timestamp field
    timestamp = models.DateTimeField(default=timezone.now)
    
    # Remaining fields as per your previous model
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    stock_price = models.FloatField(null=True, blank=True)
    revenue = models.FloatField(null=True, blank=True)
    operating_expense = models.FloatField(null=True, blank=True)
    net_income = models.FloatField(null=True, blank=True)
    net_profit_margin = models.FloatField(null=True, blank=True)
    earnings_per_share = models.FloatField(null=True, blank=True)
    ebitda = models.FloatField(null=True, blank=True)
    effective_tax_rate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.symbol

    class Meta:
        verbose_name = "Stock Data"
        db_table = 'stock_data'
