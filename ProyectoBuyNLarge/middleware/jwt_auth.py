import jwt
from django.conf import settings
from django.http import JsonResponse
from users.models import CustomUser

class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'Authorization' not in request.headers:
            return JsonResponse({'error': 'No token provided'}, status=401)

        try:
            token = request.headers['Authorization'].split(' ')[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            request.user = CustomUser.objects.get(id=payload['user_id'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token expired'}, status=401)
        except (jwt.InvalidTokenError, CustomUser.DoesNotExist):
            return JsonResponse({'error': 'Invalid token'}, status=401)

        return self.get_response(request) 