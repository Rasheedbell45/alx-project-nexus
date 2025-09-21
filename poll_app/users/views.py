from django.shortcuts import render
from django.http import JsonResponse

def profile_view(request):
    return JsonResponse({"message": "User profile endpoint"})
