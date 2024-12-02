import requests
from bs4 import BeautifulSoup
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class FetchThumbnailView(APIView):
    def post(self, request):
        url = request.data.get("url")
        if not url:
            return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # URL로부터 HTML 가져오기
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                return Response({"error": "Failed to fetch URL"}, status=status.HTTP_400_BAD_REQUEST)

            # HTML 파싱
            soup = BeautifulSoup(response.content, "html.parser")
            og_image = soup.find("meta", property="og:image")
            thumbnail_url = og_image["content"] if og_image else None

            if thumbnail_url:
                return Response({"thumbnail": thumbnail_url}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Thumbnail not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
