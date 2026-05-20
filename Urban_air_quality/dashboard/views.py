from django.shortcuts import render, redirect  # type: ignore
from django.http import JsonResponse  # type: ignore
from functools import wraps
from ml_model.predict import get_air_quality, save_data  # type: ignore


# 🔐 Reusable login decorator
def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_logged_in'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def dashboard(request):
    context = {
        'user_name': request.session.get('user_name', ''),
        'user_email': request.session.get('user_email', ''),
        'user_id': request.session.get('user_id', '')
    }
    return render(request, 'dashboard/dashboard.html', context)


def api_aqi(request):
    """
    API endpoint to fetch AQI data for a specific city.
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET request allowed'}, status=405)

    city = request.GET.get('city', '').strip()

    if not city:
        return JsonResponse({'error': 'City parameter is required'}, status=400)

    try:
        data = get_air_quality(city)

        if not data:
            return JsonResponse({'error': 'Failed to fetch AQI data'}, status=502)

        # Save only if data is valid
        save_data(city)

        return JsonResponse({
            'status': 'success',
            'city': city,
            'data': data
        })

    except Exception:
        return JsonResponse({'error': 'Internal server error'}, status=500)


@login_required
def map_view(request):
    context = {
        'user_name': request.session.get('user_name', ''),
        'user_email': request.session.get('user_email', ''),
        'user_id': request.session.get('user_id', '')
    }
    return render(request, 'dashboard/map.html', context)