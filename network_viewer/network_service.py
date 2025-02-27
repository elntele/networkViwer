# network_service.py
import time
import requests

class NetworkService:
    @staticmethod
    def get_location_data(latitude, longitude):
        time.sleep(1.5)  # Previne bloqueios da API
        url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=jsonv2"
        headers = {'User-Agent': 'GraphMapApp/1.0 (email@dominio.com)'}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json().get('display_name', 'Localização não encontrada')
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar localização: {e}")
            return None