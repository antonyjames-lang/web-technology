"""
URL configuration for yojana_mitra_backend project.
"""
from pathlib import Path
from django.contrib import admin
from django.urls import path, include, re_path
from django.http import JsonResponse, FileResponse, HttpResponseNotFound

FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / 'frontend'

def serve_frontend_index(request):
    index_path = FRONTEND_DIR / 'index.html'
    if index_path.exists():
        return FileResponse(open(index_path, 'rb'), content_type='text/html')
    return JsonResponse({
        "app": "Yojana Mitra API",
        "version": "1.0.0",
        "status": "Online",
        "description": "Government Scheme Eligibility Identifier API",
        "endpoints": {
            "taxonomy": "/api/taxonomy",
            "request_otp": "/api/auth/request-otp",
            "verify_otp": "/api/auth/verify-otp",
            "me": "/api/me",
            "profile": "/api/me/profile",
            "schemes": "/api/schemes"
        }
    })

def serve_frontend_static(request, filename):
    file_path = FRONTEND_DIR / filename
    if file_path.exists() and file_path.is_file():
        content_type = 'text/plain'
        if filename.endswith('.css'):
            content_type = 'text/css'
        elif filename.endswith('.js'):
            content_type = 'application/javascript'
        elif filename.endswith('.html'):
            content_type = 'text/html'
        return FileResponse(open(file_path, 'rb'), content_type=content_type)
    return HttpResponseNotFound("Static file not found")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', serve_frontend_index, name='frontend_index'),
    path('app', serve_frontend_index, name='frontend_app'),
    path('style.css', lambda req: serve_frontend_static(req, 'style.css')),
    path('app.js', lambda req: serve_frontend_static(req, 'app.js')),
]
