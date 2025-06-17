from django.shortcuts import render
import csv
import os
from django.conf import settings
from django.http import JsonResponse


def home(request):
    # 讀取全部資料，給前端菜單用
    csv_path = os.path.join(settings.BASE_DIR, 'app_restaurants', 'dataset', 'michelin_restaurants_processed.csv')
    restaurants = []
    cities = set()
    cuisines = set()

    if os.path.exists(csv_path):
        with open(csv_path, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                restaurants.append(row)
                cities.add(row['city'])
                cuisines.add(row['cuisine'])
    else:
        restaurants = []

    return render(request, 'app_restaurants/home.html', {
        'cities': sorted(cities),
        'cuisines': sorted(cuisines),
    })


def api_get_restaurants(request):
    data = []
    csv_path = os.path.join(settings.BASE_DIR, 'app_restaurants', 'dataset', 'michelin_restaurants_processed.csv')

    if not os.path.exists(csv_path):
        return JsonResponse({'error': '找不到資料檔案'}, status=500)

    city_query = request.GET.get('city', '')  # 多城市逗號分隔
    cuisine_query = request.GET.get('cuisine', '')  # 多菜系逗號分隔

    city_list = [c.strip() for c in city_query.split(',') if c.strip()] if city_query else []
    cuisine_list = [c.strip() for c in cuisine_query.split(',') if c.strip()] if cuisine_query else []

    with open(csv_path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if city_list and row['city'] not in city_list:
                continue
            if cuisine_list and row['cuisine'] not in cuisine_list:
                continue

            data.append({
                'name': row['name'],
                'url': row['url'],
                'address': row['address'],
                'city': row['city'],
                'price_level': row['price_level'],
                'cuisine': row['cuisine'],
                'phone': row.get('phone', ''),
                'description': row.get('description', ''),
            })

    return JsonResponse({'restaurants': data})


def api_get_cuisine_stats(request):
    csv_path = os.path.join(settings.BASE_DIR, 'app_restaurants', 'dataset', 'michelin_restaurants_processed.csv')

    if not os.path.exists(csv_path):
        return JsonResponse({'error': '找不到資料檔案'}, status=500)

    city_query = request.GET.get('city', '')  # 多城市逗號分隔
    city_list = [c.strip() for c in city_query.split(',') if c.strip()] if city_query else []

    cuisine_count = {}

    with open(csv_path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if city_list and row['city'] not in city_list:
                continue
            cuisine = row['cuisine']
            cuisine_count[cuisine] = cuisine_count.get(cuisine, 0) + 1

    cuisine_stats = [{'cuisine': k, 'count': v} for k, v in sorted(cuisine_count.items(), key=lambda x: -x[1])]

    return JsonResponse({'cuisineStats': cuisine_stats})
