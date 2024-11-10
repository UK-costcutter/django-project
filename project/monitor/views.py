from django.shortcuts import render
from django.http import JsonResponse
from .models import SystemMetrics
import psutil
import json
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'monitor/index.html')

@csrf_exempt
def toggle_monitoring(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        is_monitoring = data.get('is_monitoring', False)
        
        # Create new metric entry
        SystemMetrics.objects.create(
            cpu_usage=psutil.cpu_percent(),
            ram_usage=psutil.virtual_memory().percent,
            disk_usage=psutil.disk_usage('/').percent,
            is_monitoring=is_monitoring
        )
        return JsonResponse({'status': 'success', 'is_monitoring': is_monitoring})
    return JsonResponse({'status': 'error'}, status=400)

def get_system_metrics(request):
    # Get system metrics
    cpu_usage = psutil.cpu_percent()
    ram = psutil.virtual_memory()
    ram_usage = ram.percent
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent

    # Get monitoring status
    latest_metric = SystemMetrics.objects.first()
    is_monitoring = latest_metric.is_monitoring if latest_metric else False

    if is_monitoring:
        SystemMetrics.objects.create(
            cpu_usage=cpu_usage,
            ram_usage=ram_usage,
            disk_usage=disk_usage,
            is_monitoring=is_monitoring
        )

    # Get historical data
    historical_data = SystemMetrics.objects.filter(is_monitoring=True).order_by('-timestamp')[:60]
    
    data = {
        'current': {
            'cpu': cpu_usage,
            'ram': ram_usage,
            'disk': disk_usage,
            'is_monitoring': is_monitoring
        },
        'historical': {
            'timestamps': [metric.timestamp.strftime('%H:%M:%S') for metric in reversed(historical_data)],
            'cpu': [metric.cpu_usage for metric in reversed(historical_data)],
            'ram': [metric.ram_usage for metric in reversed(historical_data)],
            'disk': [metric.disk_usage for metric in reversed(historical_data)]
        }
    }
    return JsonResponse(data)
