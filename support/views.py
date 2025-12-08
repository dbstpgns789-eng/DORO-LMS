from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import FAQCategory, FAQItem
from .serializers import FAQCategorySerializer, FAQItemSerializer


# 1. 화면 렌더링 (HTML 보여주기)
def chatbot_page(request):
    return render(request, 'support/chatbot.html')


# 2. API 로직 (데이터 보내주기)
class ChatbotFlowView(APIView):
    def get(self, request):
        parent_id = request.query_params.get('parent_id')

        if parent_id == 'null' or parent_id == '':
            parent_id = None

        # --- [추가된 부분] 뒤로가기 ID 계산 로직 시작 ---
        back_id = None
        has_back = False

        if parent_id:  # 현재 최상위가 아니라면 항상 뒤로가기 가능
            has_back = True
            try:
                current_category = FAQCategory.objects.get(id=parent_id)
                # 부모가 있으면 그 ID로, 없으면 None(최상위)으로 설정
                if current_category.parent:
                    back_id = current_category.parent.id
                else:
                    back_id = None
            except FAQCategory.DoesNotExist:
                has_back = False
        # --- [추가된 부분] 뒤로가기 ID 계산 로직 끝 ---

        # 공통 응답 데이터 구성을 위한 함수
        def make_response(res_type, msg, data):
            return Response({
                "type": res_type,
                "message": msg,
                "data": data,
                "has_back": has_back,  # 뒤로가기 가능 여부
                "back_id": back_id     # 돌아갈 ID
            }, status=status.HTTP_200_OK)

        # 1. 하위 카테고리 확인
        sub_categories = FAQCategory.objects.filter(parent_id=parent_id)
        if sub_categories.exists():
            return make_response(
                "category",
                "원하시는 항목을 선택해 주세요.",
                FAQCategorySerializer(sub_categories, many=True).data
            )

        # 2. 질문 리스트 확인
        questions = FAQItem.objects.filter(category_id=parent_id)
        if questions.exists():
            return make_response(
                "question",
                "아래 질문 중에서 선택해 주세요.",
                FAQItemSerializer(questions, many=True).data
            )

        # 3. 데이터 없음
        return make_response("empty", "등록된 내용이 없습니다.", [])