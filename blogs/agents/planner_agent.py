import random

class PlannerAgent:
    def __init__(self):
        # 향후 Google Trends API, 검색량 분석 API 연동
        pass
        
    def generate_topic(self):
        """
        검색량이 많고 경쟁이 적은 롱테일 키워드를 발굴합니다.
        (현재는 샘플 리스트에서 랜덤 반환)
        """
        sample_topics = [
            "2024년 직장인 부업 추천 TOP 5",
            "초보자도 따라하는 챗GPT 수익화 방법",
            "블로그 SEO 최적화 가이드라인 10가지",
            "미국 주식 배당주 투자 전략"
        ]
        topic = random.choice(sample_topics)
        return topic
