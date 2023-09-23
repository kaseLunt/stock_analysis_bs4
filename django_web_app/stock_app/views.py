from django.shortcuts import render
from .models import StockData

def stock_dashboard(request):
    stocks = StockData.objects.all()
    return render(request, 'dashboard.html', {'stocks': stocks})
