from shared.config.env import OPENAI_API_KEY
from openai import OpenAI
import json

client = OpenAI(api_key=OPENAI_API_KEY)

def classify_deals(deals: list[dict]) -> dict:
    category_list = "\n".join([
        "1. 패션잡화", "2. 뷰티/미용", "3. 유아동/출산", "4. 식품/건강식품",
        "5. 주방/조리도구", "6. 생활/건강", "7. 홈데코/인테리어", "8. 가전/디지털기기",
        "9. 스포츠/아웃도어", "10. 자동차/공구", "11. 도서/음반", "12. 완구/취미용품",
        "13. 문구/사무용품", "14. 반려동물", "15. 헬스/건강", "16. 여행/티켓"
    ])
    items = "\n".join([
        f"- deal_no: {d['deal_no']}\n  제목: {d['title']}\n  내용: {d['content']}"
        for d in deals
    ])
    prompt = f"""
당신은 상품 정보를 한국 이커머스 사이트의 카테고리로 분류하는 분류 시스템입니다.

다음 1~16번 카테고리 중에서 각 상품의 제목과 내용을 참고해 가장 적절한 번호를 분류하세요.

카테고리 목록:
{category_list}

상품 목록:
{items}

JSON 형식으로 결과만 출력하세요.
예시:
{{
  "8392990746": 4,
  "8392990789": 8
}}

오직 JSON 결과만 주세요.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # ✅ 이 줄만 바뀜
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )

    content = response.choices[0].message.content
    return json.loads(content)
