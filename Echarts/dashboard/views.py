from __future__ import annotations

import random
from datetime import date, timedelta

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET


def dashboard(request):
    return render(request, "dashboard.html")


@require_GET
def api_line_bar(request):
    """
    Returns categories + series for a combined line + bar chart.
    """
    days = int(request.GET.get("days", "30"))
    end = date.today()
    start = end - timedelta(days=days - 1)

    x = [(start + timedelta(days=i)).isoformat() for i in range(days)]
    revenue = [200 + i * 7 + random.randint(-25, 25) for i in range(days)]
    orders = [80 + random.randint(-15, 15) for _ in range(days)]

    return JsonResponse(
        {
            "x": x,
            "series": [
                {"name": "Revenue", "type": "line", "data": revenue, "smooth": True},
                {"name": "Orders", "type": "bar", "data": orders},
            ],
        }
    )


@require_GET
def api_scatter(request):
    """
    Returns many [x,y] points for a scatter plot.
    """
    n = int(request.GET.get("n", "100"))
    points = [[random.random() * 100, random.random() * 100] for _ in range(n)]
    return JsonResponse({"points": points})


@require_GET
def api_radar(request):
    """
    Returns a radar chart config payload.
    """
    indicators = [
        {"name": "Quality", "max": 100},
        {"name": "Speed", "max": 100},
        {"name": "Reliability", "max": 100},
        {"name": "Cost", "max": 100},
        {"name": "Support", "max": 100},
    ]
    values1 = [82, 74, 88, 61, 79]
    values2 = [33, 4, 12, 19, 30]

    return JsonResponse(
        {
            "indicators": indicators,
            "series": [
                {"name": "S1", "data": values1},
                {"name": "S2", "data": values2},
            ],
        }
    )
    #return JsonResponse({"indicators": indicators, "values": values})