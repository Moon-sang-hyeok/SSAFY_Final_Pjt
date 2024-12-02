import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

api_key = settings.VITE_KAKAO_MAP_API_KEY  # Kakao API Key

class NearbyBanksView(APIView):
    

    def get(self, request):
        lat = float(request.GET.get('lat'))
        lng = float(request.GET.get('lng'))

        # Kakao Maps API를 사용하여 주변 은행 검색
        url = "https://dapi.kakao.com/v2/local/search/keyword.json"
        headers = {
            "Authorization": f"KakaoAK {api_key}"
        }
        params = {
            "query": "은행",  # 검색할 키워드 (은행)
            "x": lng,  # 경도 (longitude)
            "y": lat,  # 위도 (latitude)
            "radius": 5000  # 5km 이내
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            nearby_banks = []

            for place in data.get('documents', []):
                bank_info = {
                    'name': place.get('place_name'),
                    'address': place.get('road_address_name', '주소 없음'),
                    'distance': place.get('distance', '정보 없음'),
                }
                nearby_banks.append(bank_info)

            return Response(nearby_banks)
        else:
            return Response({"error": "Failed to retrieve data from Kakao API"}, status=response.status_code)
