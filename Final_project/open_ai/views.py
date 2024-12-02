import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import openai
import traceback
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY
class OPENAPIView(APIView):
    def post(self, request, format=None):
        try:
            # OpenAI API 요청
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # 사용할 모델을 지정합니다.
                messages=[
                    {"role": "user", "content": "오늘의 운세를 알려줘"}
                ],
                max_tokens=1000
            )

            # OpenAI API 응답 처리
            # OpenAI의 응답에서 직접적으로 상태 코드를 확인할 수 없으므로, 예외 처리로 대응합니다.
            fortune_text = response['choices'][0]['message']['content'].strip()
            return Response({"fortune": fortune_text}, status=status.HTTP_200_OK)

        except openai.error.OpenAIError as e:
            # OpenAI API 관련 오류 처리
            error_message = str(e)
            print("OpenAI Error:", error_message)
            print(traceback.format_exc())  # 오류 트레이스백 출력
            return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            # 다른 예외 처리
            error_message = str(e)
            print("Error:", error_message)
            print(traceback.format_exc())  # 오류 트레이스백 출력
            return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)