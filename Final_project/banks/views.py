from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Bank  # 은행 모델 (예시)
from geopy.distance import geodesic

class NearbyBanksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        lat = float(request.GET.get('lat'))
        lng = float(request.GET.get('lng'))
        
        # 근처 은행을 찾는 로직 (예시)
        nearby_banks = []
        all_banks = Bank.objects.all()

        for bank in all_banks:
            bank_location = (bank.latitude, bank.longitude)
            user_location = (lat, lng)
            distance = geodesic(user_location, bank_location).km  # 거리 계산 (단위: km)

            if distance <= 5:  # 5km 이내의 은행만 가져오기
                nearby_banks.append({
                    'name': bank.name,
                    'address': bank.address,
                    'distance': distance,
                })

        return Response(nearby_banks)
