import openai


response = openai.ChatCompletion.create(
    model="gpt-4o-mini",  # 사용할 모델을 지정합니다.
    messages=[
        {"role": "user", "content":
            "ㅎㅇㅎㅇ"
        }
    ],
    max_tokens=1000
)


print(response['choices'][0]['message']['content'].strip())  #