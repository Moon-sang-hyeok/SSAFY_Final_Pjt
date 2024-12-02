# portfolio/views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Portfolio
from .serializers import PortfolioSerializer
from rest_framework.permissions import IsAuthenticated

# portfolio/views.py
@api_view(['POST'])
def create_portfolio(request):
    """
    사용자가 AI 추천 상품을 포트폴리오에 추가
    """
    if not request.user.is_authenticated:
        return Response({"detail": "로그인 후 이용해 주세요."}, status=status.HTTP_401_UNAUTHORIZED)

    # 요청된 데이터 출력
    print("Request Data:", request.data)

    product_name = request.data.get('product_name')
    bank = request.data.get('bank')
    interest_rate = request.data.get('interest_rate')

    # 포트폴리오 생성
    portfolio_data = {
        'user': request.user.id,
        'product_name': product_name,
        'bank': bank,
        'interest_rate': interest_rate,
    }

    serializer = PortfolioSerializer(data=portfolio_data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_portfolio(request):
    """
    사용자가 저장한 포트폴리오 조회
    """
    if not request.user.is_authenticated:
        return Response({"detail": "로그인 후 이용해 주세요."}, status=status.HTTP_401_UNAUTHORIZED)
    
    portfolios = Portfolio.objects.filter(user=request.user)
    serializer = PortfolioSerializer(portfolios, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_portfolio(request, pk):
    """
    사용자가 포트폴리오에서 상품을 삭제
    """
    try:
        portfolio_item = Portfolio.objects.get(id=pk, user=request.user)  # 해당 사용자의 포트폴리오만 삭제 가능
    except Portfolio.DoesNotExist:
        return Response({"detail": "포트폴리오 항목을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
    
    portfolio_item.delete()
    return Response({"detail": "포트폴리오 항목이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)