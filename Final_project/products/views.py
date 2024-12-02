
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
import requests
from rest_framework import status
from .models import SavingProducts, DepositProducts
from .serializers import SavingProductsSerializer,DepositProductsSerializer, CombinedProductSerializer
from django.conf import settings
from django.http import JsonResponse
from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticated
from accounts.models import CustomUser


class CombinedProductView(APIView):
    def get(self, request):
        # SavingProducts와 DepositProducts 데이터를 가져옵니다.
        savings = SavingProducts.objects.all()
        deposits = DepositProducts.objects.all()

        # CombinedProductSerializer로 두 모델의 데이터를 묶어서 반환합니다.
        serializer = CombinedProductSerializer({
            'savings': savings,
            'deposits': deposits
        })

        return Response(serializer.data, status=status.HTTP_200_OK)

# Create your views here.
class JoinSavingProductView(APIView):
    permission_classes = [IsAuthenticated]  # 로그인한 사용자만 접근 가능

    def post(self, request, product_id):
        try:
            # 상품 가져오기
            saving_product = SavingProducts.objects.get(id=product_id)
            
            # 현재 사용자 가져오기
            user = request.user

            # 사용자가 이미 해당 상품에 가입했는지 확인
            if saving_product in user.saving_products.all():
                return Response({"message": "이미 가입된 상품입니다."}, status=status.HTTP_400_BAD_REQUEST)

            # 상품을 사용자와 연결
            user.saving_products.add(saving_product)

            return Response({"message": "상품 가입이 완료되었습니다."}, status=status.HTTP_200_OK)
        except SavingProducts.DoesNotExist:
            return Response({"error": "해당 상품이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)


class JoinDepositProductView(APIView):
    permission_classes = [IsAuthenticated]  # 로그인한 사용자만 접근 가능

    def post(self, request, product_id):
        try:
            # 상품 가져오기
            deposit_product = DepositProducts.objects.get(id=product_id)
            
            # 현재 사용자 가져오기
            user = request.user

            # 사용자가 이미 해당 상품에 가입했는지 확인
            if deposit_product in user.deposit_products.all():
                return Response({"message": "이미 가입된 상품입니다."}, status=status.HTTP_400_BAD_REQUEST)

            # 상품을 사용자와 연결
            user.deposit_products.add(deposit_product)

            return Response({"message": "상품 가입이 완료되었습니다."}, status=status.HTTP_200_OK)
        except DepositProducts.DoesNotExist:
            return Response({"error": "해당 상품이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

# --------------------------


class SavingProductsView(APIView):
    def get(self, request):
        api_key = settings.API_KEY
        base_url = "http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json"

        # 첫 페이지 데이터 가져오기
        api_url = f"{base_url}?auth={api_key}&topFinGrpNo=020000&pageNo=1"
        response = requests.get(api_url)
        data = response.json()

        if 'result' not in data or 'max_page_no' not in data['result']:
            return Response({"error": "Invalid data received from API"}, status=status.HTTP_400_BAD_REQUEST)

        max_page_no = int(data['result']['max_page_no'])
        all_base_items = []
        all_option_items = []

        # 모든 페이지 데이터 가져오기
        for page_no in range(1, max_page_no + 1):
            api_url = f"{base_url}?auth={api_key}&topFinGrpNo=020000&pageNo={page_no}"
            response = requests.get(api_url)
            page_data = response.json()

            if 'result' in page_data:
                all_base_items.extend(page_data['result'].get('baseList', []))
                all_option_items.extend(page_data['result'].get('optionList', []))

        # 중복된 항목을 필터링하기
        all_base_items = list({(item['fin_prdt_cd'], item['fin_co_no']): item for item in all_base_items}.values())

        all_option_items = list({(item['fin_prdt_cd'], item['fin_co_no'], item['save_trm']): item for item in all_option_items}.values())

        # DB에 저장
        for base_item in all_base_items:
            fin_prdt_cd = base_item.get('fin_prdt_cd')
            fin_co_no = base_item.get('fin_co_no')
            join_way = base_item.get('join_way', '')
            spcl_cnd = base_item.get('spcl_cnd', '')
            join_member = base_item.get('join_member', '')
            kor_co_nm = base_item.get('kor_co_nm', '')
            max_limit = base_item.get('max_limit', '')

            # 해당 상품의 옵션 데이터 필터링
            product_options = [
                option for option in all_option_items
                if option['fin_prdt_cd'] == fin_prdt_cd and option['fin_co_no'] == fin_co_no
            ]

            for option in product_options:
                intr_rate = option.get('intr_rate', 0)
                intr_rate2 = option.get('intr_rate2', 0)
                intr_rate_type_nm = option.get('intr_rate_type_nm', '')
                rsrv_type_nm = option.get('rsrv_type_nm', '')
                save_trm = option.get('save_trm', 0)

                try:
                    # 기존 상품이 있으면 업데이트, 없으면 새로 생성
                    SavingProducts.objects.update_or_create(
                        fin_prdt_cd=fin_prdt_cd,
                        fin_co_no=fin_co_no,
                        fin_prdt_nm=base_item.get('fin_prdt_nm', ''),
                        save_trm=save_trm,  # save_trm을 기준으로 업데이트
                        defaults={
                            'join_way': join_way,
                            'spcl_cnd': spcl_cnd,
                            'join_member': join_member,
                            'intr_rate': intr_rate,
                            'intr_rate2': intr_rate2,
                            'intr_rate_type_nm': intr_rate_type_nm,
                            'rsrv_type_nm': rsrv_type_nm,
                            'kor_co_nm':kor_co_nm,
                            'max_limit':max_limit
                        }
                    )
                    
                except IntegrityError as e:
                    print(f"IntegrityError: {e} for {fin_prdt_cd} - {fin_co_no} - {save_trm}")

        # 응답 데이터
        products = SavingProducts.objects.all()
        serializer = SavingProductsSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
def savings_comparison_api(request):
    products = SavingProducts.objects.all().values()  # 데이터베이스의 모든 데이터를 가져옵니다.
    return JsonResponse(list(products), safe=False)  # JSON으로 반환

class SavingDetailView(APIView):
    def get(self, request, product_id):
        try:
            product = SavingProducts.objects.get(id=product_id)
            serializer = SavingProductsSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SavingProducts.DoesNotExist:
            return Response({"error": "SavingProducts not found"}, status=status.HTTP_404_NOT_FOUND)
        


class DepositProductsView(APIView):
    def get(self, request):
        api_key = settings.API_KEY
        base_url = "http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"

        # 첫 페이지 데이터 가져오기
        api_url = f"{base_url}?auth={api_key}&topFinGrpNo=020000&pageNo=1"
        response = requests.get(api_url)
        data = response.json()

        if 'result' not in data or 'max_page_no' not in data['result']:
            return Response({"error": "Invalid data received from API"}, status=status.HTTP_400_BAD_REQUEST)

        max_page_no = int(data['result']['max_page_no'])
        all_base_items = []
        all_option_items = []

        # 모든 페이지 데이터 가져오기
        for page_no in range(1, max_page_no + 1):
            api_url = f"{base_url}?auth={api_key}&topFinGrpNo=020000&pageNo={page_no}"
            response = requests.get(api_url)
            page_data = response.json()

            if 'result' in page_data:
                all_base_items.extend(page_data['result'].get('baseList', []))
                all_option_items.extend(page_data['result'].get('optionList', []))

        # 중복된 항목을 필터링하기
        all_base_items = list({(item['fin_prdt_cd'], item['fin_co_no']): item for item in all_base_items}.values())
        all_option_items = list({(item['fin_prdt_cd'], item['fin_co_no'], item['save_trm']): item for item in all_option_items}.values())


        # DB에 저장
        for base_item in all_base_items:
            fin_prdt_cd = base_item.get('fin_prdt_cd')
            fin_co_no = base_item.get('fin_co_no')
            join_way = base_item.get('join_way', '')
            spcl_cnd = base_item.get('spcl_cnd', '')
            join_member = base_item.get('join_member', '')
            kor_co_nm = base_item.get('kor_co_nm', '')
            max_limit = base_item.get('max_limit', '')

            # 해당 상품의 옵션 데이터 필터링
            product_options = [
                option for option in all_option_items
                if option['fin_prdt_cd'] == fin_prdt_cd and option['fin_co_no'] == fin_co_no 
            ]
            for option in product_options:
                intr_rate = option.get('intr_rate', 0)
                intr_rate2 = option.get('intr_rate2', 0)
                intr_rate_type_nm = option.get('intr_rate_type_nm', '')
                save_trm = option.get('save_trm', 0)

                try:
                    # 기존 상품이 있으면 업데이트, 없으면 새로 생성
                    DepositProducts.objects.update_or_create(
                        fin_prdt_cd=fin_prdt_cd,
                        fin_co_no=fin_co_no,
                        fin_prdt_nm=base_item.get('fin_prdt_nm', ''),
                        save_trm=save_trm,  # save_trm을 기준으로 업데이트
                        defaults={
                            'join_way': join_way,
                            'spcl_cnd': spcl_cnd,
                            'join_member': join_member,
                            'intr_rate': intr_rate,
                            'intr_rate2': intr_rate2,
                            'intr_rate_type_nm': intr_rate_type_nm,
                            'kor_co_nm':kor_co_nm,
                            'max_limit':max_limit
                        }
                    )
                    
                except IntegrityError as e:
                    print(f"IntegrityError: {e} for {fin_prdt_cd} - {fin_co_no} - {save_trm}")

        # 응답 데이터
        products = DepositProducts.objects.all()
        serializer = DepositProductsSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
def deposit_comparison_api(request):
    products = DepositProducts.objects.all().values()  # 데이터베이스의 모든 데이터를 가져옵니다.
    return JsonResponse(list(products), safe=False)  # JSON으로 반환

class DepositDetailView(APIView):
    def get(self, request, product_id):
        try:
            product = DepositProducts.objects.get(id=product_id)
            serializer = DepositProductsSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DepositProducts.DoesNotExist:
            return Response({"error": "DepositProducts not found"}, status=status.HTTP_404_NOT_FOUND)
