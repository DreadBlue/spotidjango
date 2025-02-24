import os
from django.views import View
from rest_framework import viewsets
from .models import User
import base64
from django.http import JsonResponse
import json
import requests
from .serializers import UserSerializer

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SpotiApiView(View):
    def post(self, request):
        body = json.loads(request.body)
        cancion = body.get("cancion")
        correo = body.get("correo")
        url = 'https://accounts.spotify.com/api/token'
        auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
        b64_auth = base64.b64encode(auth_str.encode()).decode()

        headers = {
            "Authorization": f"Basic {b64_auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {"grant_type": "client_credentials"}

        response = requests.post(url, headers=headers, data=data)
        token_info = response.json().get("access_token")

        if not token_info:
            return {"message": "No se ha podido obtener el token"}

        search_url = f"https://api.spotify.com/v1/search?q={cancion}&type=track&limit=1"
        headers = {"Authorization": f"Bearer {token_info}"}

        response = requests.get(search_url, headers=headers)
        data = response.json()

        cancion_data = data["tracks"]["items"][0]
        cancion_info = {
            "nombre": cancion_data["name"],
            "artista": cancion_data["artists"][0]["name"],
            "url": cancion_data["external_urls"]["spotify"]
        }

        try:
            data = json.loads(request.body)
            if not correo or not cancion_info:
                return JsonResponse({"message": "Faltan datos requeridos"}, status=400)

            try:
                user = User.objects.get(correo=correo)
            except User.DoesNotExist:
                return JsonResponse({"message": "Usuario no encontrado"}, status=404)

            if not isinstance(user.canciones, list):
                user.canciones = [] 

            user.canciones.append(cancion_info) 
            user.save()

            return JsonResponse({"message": "Canción agregada con éxito"})

        except json.JSONDecodeError:
            return JsonResponse({"message": "Error en el formato JSON"}, status=400)
