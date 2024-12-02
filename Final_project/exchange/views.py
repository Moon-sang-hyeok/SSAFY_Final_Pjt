import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import logging
from datetime import datetime, timedelta

API_KEY = settings.FOREX_API_KEY  # API 키를 settings에서 가져옴
logger = logging.getLogger(__name__)

class ExchangeRateView(APIView):
    def get(self, request):
        # 오전 10시 이전에는 어제 날짜로 설정
        now = datetime.now()
        if now.hour < 10:
            target_date = (now - timedelta(days=1)).strftime('%Y%m%d')
        else:
            target_date = now.strftime('%Y%m%d')

        # API 요청 URL
        url = f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={API_KEY}"
        params = {
            'searchdate': target_date,  # 위에서 계산한 날짜로 요청
            'data': 'AP01',  # 요청 데이터 유형
        }

        try:
            # API 호출
            response = requests.get(url, params=params, timeout=20, verify=False)

            if response.status_code == 200:
                data = response.json()  # JSON 데이터를 리스트로 반환

                # 예상치 못한 데이터 구조 처리
                if isinstance(data, list):
                    # 'result' 필드가 3인 경우는 에러 상황으로 처리
                    if all(item.get("result") == 3 for item in data):
                        logger.error("API returned no data or error in response.")
                        return Response(
                            {"error": "API returned no data.", "details": data},
                            status=status.HTTP_204_NO_CONTENT,
                        )

                    # 필요한 통화 데이터 추출
                    exchange_rates = {
                        '미국 USD': next(((item['deal_bas_r']) for item in data if item['cur_unit'] == 'USD'), '데이터 없음'),
                        '유럽 EUR': next((item['deal_bas_r'] for item in data if item['cur_unit'] == 'EUR'), '데이터 없음'),
                        '일본 JPY': next((str(round((float(item['deal_bas_r'] ) / 100), 2)) for item in data if item['cur_unit'] == 'JPY(100)'), '데이터 없음'),
                        '중국 CNY': next((item['deal_bas_r'] for item in data if item['cur_unit'] == 'CNH'), '데이터 없음'),
                        '한국 KRW': next((item['deal_bas_r'] for item in data if item['cur_unit'] == 'KRW'), '데이터 없음'),
                        '호주 AUD': next((item['deal_bas_r'] for item in data if item['cur_unit'] == 'AUD'), '데이터 없음'),
                        '영국 GBP': next((item['deal_bas_r'] for item in data if item['cur_unit'] == 'GBP'), '데이터 없음'),
                        '태국 THB': next((item['deal_bas_r'] for item in data if item['cur_unit'] == 'THB'), '데이터 없음'),
                    }
                    return Response(exchange_rates, status=status.HTTP_200_OK)
                else:
                    logger.error(f"Unexpected data format: {data}")
                    return Response({"error": "Unexpected data format."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            else:
                logger.error(f"환율 API 요청 실패: {response.status_code} - {response.text}")
                return Response(
                    {"error": "Failed to fetch exchange rates.", "details": response.text},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        except requests.exceptions.RequestException as e:
            logger.error(f"환율 API 호출 중 오류 발생: {str(e)}")
            return Response(
                {"error": "Error occurred while fetching exchange rates.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )