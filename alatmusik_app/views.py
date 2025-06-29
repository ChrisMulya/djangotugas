from django.shortcuts import render
from django.http import JsonResponse

def canary_view(request):
    """
    View sederhana untuk mendiagnosis method request yang diterima oleh Django.
    """
    return JsonResponse({
        'message': 'Canary view berhasil dijangkau!',
        'method_diterima': request.method
    })
