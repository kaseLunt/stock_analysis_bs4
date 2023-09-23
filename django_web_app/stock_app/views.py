from django.db.models import Max, F
from django.shortcuts import render
from .models import StockData


def stock_dashboard(request):
    # Annotate the latest timestamp for each unique symbol
    latest_stocks = StockData.objects.values('symbol').annotate(latest_timestamp=Max('timestamp'))

    # Initialize an empty QuerySet
    queryset = StockData.objects.none()

    # Loop over each annotated stock to filter the latest entry for each symbol
    for stock in latest_stocks:
        latest_for_symbol = StockData.objects.filter(
            symbol=stock['symbol'],
            timestamp=stock['latest_timestamp']
        )
        queryset = queryset | latest_for_symbol

    return render(request, 'dashboard.html', {'stocks': queryset})
