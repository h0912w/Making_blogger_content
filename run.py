#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO Blog AI Optimizer 실행 스크립트
더블클릭하여 실행 가능

작성일: 2026-03-06
버전: 2.0.0
"""

import os
import sys
import re
import time
from typing import Optional, Dict, Tuple

# Windows UTF-8 설정
if sys.platform == 'win32':
    import locale
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# 현재 파일 위치를 기준으로 경로 설정
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# 상수 설정
MAX_RETRIES = 3
ANALYSIS_PASS_THRESHOLD = 70
TITLE_PASS_THRESHOLD = 35
CONTENT_PASS_THRESHOLD = 35


class Colors:
    """터미널 색상 클래스"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """헤더 출력"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{text}{Colors.END}")
    print("=" * 60)


def print_success(text: str):
    """성공 메시지 출력"""
    print(f"{Colors.GREEN}[OK] {text}{Colors.END}")


def print_error(text: str):
    """에러 메시지 출력"""
    print(f"{Colors.RED}[ERROR] {text}{Colors.END}")


def print_info(text: str):
    """정보 메시지 출력"""
    print(f"{Colors.BLUE}[INFO] {text}{Colors.END}")


def print_warning(text: str):
    """경고 메시지 출력"""
    print(f"{Colors.YELLOW}[WARN] {text}{Colors.END}")


def read_file(filepath: str) -> Optional[str]:
    """
    파일 읽기

    Args:
        filepath: 파일 경로

    Returns:
        파일 내용 또는 None
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            return content if content.strip() else None
    except FileNotFoundError:
        print_error(f"{filepath} 파일을 찾을 수 없습니다.")
        return None
    except Exception as e:
        print_error(f"파일 읽기 오류: {e}")
        return None


def write_file(filepath: str, content: str) -> bool:
    """
    파일 쓰기

    Args:
        filepath: 파일 경로
        content: 저장할 내용

    Returns:
        성공 여부
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print_success(f"결과가 저장되었습니다: {filepath}")
        return True
    except Exception as e:
        print_error(f"파일 쓰기 실패: {e}")
        return False


def extract_api_key(api_key_content: str) -> Optional[str]:
    """
    API Key 추출

    Args:
        api_key_content: API Key 파일 내용

    Returns:
        API Key 또는 None
    """
    # 여러 형식 시도
    patterns = [
        r'\[([^\]]+)\]',      # [key] 형식
        r'key:\s*([^\s\n]+)',  # key: value 형식
        r'([a-f0-9]+\.[a-zA-Z0-9]+)',  # GLM key 형식
    ]

    for pattern in patterns:
        match = re.search(pattern, api_key_content)
        if match:
            key = match.group(1).strip()
            if key and key not in ['API Key 여기에 입력', 'your_api_key_here']:
                return key
    return None


def check_dependencies() -> bool:
    """
    필요한 라이브러리 확인

    Returns:
        설치 여부
    """
    try:
        import anthropic
        return True
    except ImportError:
        return False


def create_prompt(input_content: str, seo_rules: str, ai_rules: str) -> str:
    """
    AI 프롬프트 생성

    Args:
        input_content: 입력 콘텐츠
        seo_rules: SEO 규칙
        ai_rules: AI 검색 규칙

    Returns:
        생성된 프롬프트
    """
    # SEO 규칙 처리
    seo_summary = seo_rules[:2000] if seo_rules and len(seo_rules) > 2000 else (seo_rules if seo_rules else "기본: 제목 60자 이내, 클릭 유도, 핵심 키워드 포함")

    # AI 규칙 처리
    ai_summary = ai_rules[:2000] if ai_rules and len(ai_rules) > 2000 else (ai_rules if ai_rules else "기본: 직접적인 답변 제공, 구조화된 정보, 출처 표기")

    prompt = f"""당신은 SEO 및 AI 검색 노출 전문가입니다.

다음 정보를 바탕으로 최적화된 블로그 글 제목과 본문 가이드를 생성해주세요.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[글 설명]
{input_content}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[SEO 규칙 요약]
{seo_summary}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[AI 검색 노출 규칙 요약]
{ai_summary}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

요구사항:
1. 제목은 60자 이내, 클릭 유도, 핵심 키워드 포함, 경험 기반 표현
2. 본문은 H2/H3 구조, 키워드 자연스러운 배치, 3-5문장 단락
3. AI 검색 엔진이 쉽게 인용할 수 있는 직접적인 답변 형식
4. E-E-A-T 요소 강화 (경험, 전문성, 권위성, 신뢰성)
5. 구조화된 정보 (불릿 포인트, 표, 번호 매기기) 활용
6. FAQ 섹션 포함 (AI 인용 최적화)
7. 한국어로 작성

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

아래 형식에 맞춰 결과를 출력해주세요:

[제목] 최적화된 제목

[본문에 포함될 핵심 키워드]
- 메인 키워드
- 관련 키워드 1
- 관련 키워드 2
- 롱테일 키워드

[본문 구성 가이드]

## 1. 도입부 (AI 검색 친화적)
- 첫 단락: 직접적인 답변/요약
- 상세 설명: 배경 정보, 중요성
- 훅: 독자의 관심 유도 요소

## 2. 본문 (SEO 최적화)
- H2 섹션 1: 주요 내용
  - H3 세부 내용
  - 불릿 포인트/예시
- H2 섹션 2: 실전 팁/가이드
  - 단계별 설명
  - 코드 예시/스크린샷
- H2 섹션 3: 추가 정보

## 3. FAQ 섹션 (AI 인용 최적화)
### Q: 질문 1?
**A:** 직접적인 답변

### Q: 질문 2?
**A:** 직접적인 답변

## 4. 결론
- 핵심 요약
- 추가 리소스 링크
- 행동 유도 (CTA)

[SEO 점검 리스트]
- 제목 길이: __/60 자 [OK]
- 메타디스크립션: 150-160자 제안
- 키워드 밀도: 1-2% 자연스러운 배치
- H2/H3 구조: 포함 [OK]
- 불릿 포인트: 활용 [OK]
- 내부 링크: 기회 파악

[AI 검색 노출 팁]
- FAQ Schema 적용 권장
- 구조화된 데이터 (JSON-LD) 제안
- 출처 표기 방법
- 인용 가능한 형식 (구체적 수치, 예시)

[추가 제안]
- 관련 주제 추천
- 연계 글 제안
- 콘텐츠 길이 조절 (1,500-3,000자)
"""
    return prompt


def call_api(api_key: str, prompt: str) -> Optional[str]:
    """
    GLM-5 API 호출

    Args:
        api_key: API Key
        prompt: 프롬프트

    Returns:
        API 응답 또는 None
    """
    try:
        import anthropic

        print_info("API 연결 중...")

        client = anthropic.Anthropic(
            api_key=api_key,
            base_url="https://api.z.ai/api/anthropic",
            timeout=120  # 2분 타임아웃
        )

        print_info("콘텐츠 생성 중... (약 30~60초 소요)")

        start_time = time.time()

        response = client.messages.create(
            model="glm-4.7",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        elapsed_time = time.time() - start_time
        print_success(f"API 응답 완료 ({elapsed_time:.1f}초)")

        return response.content[0].text

    except anthropic.AuthenticationError:
        print_error("인증 실패: API Key를 확인해주세요.")
        return None
    except anthropic.RateLimitError:
        print_error("요청 한도 초과: 잠시 후 다시 시도해주세요.")
        return None
    except anthropic.APITimeoutError:
        print_error("API 요청 시간 초과: 다시 시도해주세요.")
        return None
    except Exception as e:
        print_error(f"API 호출 실패: {e}")
        return None


def create_generation_prompt(input_content: str, seo_rules: str, ai_rules: str, previous_feedback: str = "") -> str:
    """
    콘텐츠 생성 프롬프트 생성 (제목 5개 + 한/영 버전)

    Args:
        input_content: 입력 콘텐츠
        seo_rules: SEO 규칙
        ai_rules: AI 검색 규칙
        previous_feedback: 이전 피드백 (재생성 시)

    Returns:
        생성된 프롬프트
    """
    # SEO 규칙 처리
    seo_summary = seo_rules[:2000] if seo_rules and len(seo_rules) > 2000 else (seo_rules if seo_rules else "기본: 제목 60자 이내, 클릭 유도, 핵심 키워드 포함")

    # AI 규칙 처리
    ai_summary = ai_rules[:2000] if ai_rules and len(ai_rules) > 2000 else (ai_rules if ai_rules else "기본: 직접적인 답변 제공, 구조화된 정보, 출처 표기")

    # 피드백 추가 (있는 경우)
    feedback_section = f"\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n[이전 피드백 반영]\n{previous_feedback}" if previous_feedback else ""

    prompt = f"""당신은 SEO 및 AI 검색 노출 전문가입니다.

다음 정보를 바탕으로 최적화된 블로그 글 제목 5개와 본문 가이드를 한국어와 영어로 생성해주세요.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[글 설명]
{input_content}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[SEO 규칙 요약]
{seo_summary}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[AI 검색 노출 규칙 요약]
{ai_summary}
{feedback_section}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

요구사항:
1. 제목은 5개 제안하며, 각 제목에 예상 클릭률(High/Medium/Low), SEO 점수(0-100), 설명 포함
2. 5개의 제목은 다른 각도로 구성 (질문형, 숫자형, 혜택형, 궁금증형, 긴급형 등)
3. 본문은 한국어와 영어 두 버전으로 생성
4. 본문은 H2/H3 구조, 키워드 자연스러운 배치, 3-5문장 단락
5. AI 검색 엔진이 쉽게 인용할 수 있는 직접적인 답변 형식
6. E-E-A-T 요소 강화 (경험, 전문성, 권위성, 신뢰성)
7. 구조화된 정보 (불릿 포인트, 표, 번호 매기기) 활용
8. FAQ 섹션 포함 (AI 인용 최적화)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

아래 형식에 맞춰 결과를 출력해주세요:

# SEO 최적화 블로그 글 가이드

## [한국어 버전]

### === 제목 추천 (5개) ===

1. **제목**
   - 예상 클릭률: High/Medium/Low
   - SEO 점수: 0-100
   - 설명: 제목 선택 이유 및 특징

2. **제목**
   - 예상 클릭률: High/Medium/Low
   - SEO 점수: 0-100
   - 설명: 제목 선택 이유 및 특징

3. **제목**
   - 예상 클릭률: High/Medium/Low
   - SEO 점수: 0-100
   - 설명: 제목 선택 이유 및 특징

4. **제목**
   - 예상 클릭률: High/Medium/Low
   - SEO 점수: 0-100
   - 설명: 제목 선택 이유 및 특징

5. **제목**
   - 예상 클릭률: High/Medium/Low
   - SEO 점수: 0-100
   - 설명: 제목 선택 이유 및 특징

### === 본문 구성 가이드 ===

#### 본문에 포함될 핵심 키워드
- 메인 키워드
- 관련 키워드 1
- 관련 키워드 2
- 롱테일 키워드

#### 1. 도입부 (AI 검색 친화적)
- 첫 단락: 직접적인 답변/요약
- 상세 설명: 배경 정보, 중요성
- 훅: 독자의 관심 유도 요소

#### 2. 본문 (SEO 최적화)
- H2 섹션 1: 주요 내용
  - H3 세부 내용
  - 불릿 포인트/예시
- H2 섹션 2: 실전 팁/가이드
  - 단계별 설명
  - 코드 예시/스크린샷
- H2 섹션 3: 추가 정보

#### 3. FAQ 섹션 (AI 인용 최적화)
### Q: 질문 1?
**A:** 직접적인 답변

### Q: 질문 2?
**A:** 직접적인 답변

#### 4. 결론
- 핵심 요약
- 추가 리소스 링크
- 행동 유도 (CTA)

#### SEO 점검 리스트
- 제목 길이: __/60 자 [OK]
- 메타디스크립션: 150-160자 제안
- 키워드 밀도: 1-2% 자연스러운 배치
- H2/H3 구조: 포함 [OK]
- 불릿 포인트: 활용 [OK]
- 내부 링크: 기회 파악

#### AI 검색 노출 팁
- FAQ Schema 적용 권장
- 구조화된 데이터 (JSON-LD) 제안
- 출처 표기 방법
- 인용 가능한 형식 (구체적 수치, 예시)

## [English Version]

### === Title Recommendations (5) ===

1. **Title**
   - Expected CTR: High/Medium/Low
   - SEO Score: 0-100
   - Description: Reason and characteristics

2. **Title**
   - Expected CTR: High/Medium/Low
   - SEO Score: 0-100
   - Description: Reason and characteristics

3. **Title**
   - Expected CTR: High/Medium/Low
   - SEO Score: 0-100
   - Description: Reason and characteristics

4. **Title**
   - Expected CTR: High/Medium/Low
   - SEO Score: 0-100
   - Description: Reason and characteristics

5. **Title**
   - Expected CTR: High/Medium/Low
   - SEO Score: 0-100
   - Description: Reason and characteristics

### === Body Content Guide ===

#### Key Keywords to Include
- Main keyword
- Related keyword 1
- Related keyword 2
- Long-tail keyword

#### 1. Introduction (AI Search Friendly)
- First paragraph: Direct answer/summary
- Detailed explanation: Background, importance
- Hook: Element to engage readers

#### 2. Body (SEO Optimized)
- H2 Section 1: Main content
  - H3 Details
  - Bullet points/examples
- H2 Section 2: Practical tips/guide
  - Step-by-step explanation
  - Code examples/screenshots
- H2 Section 3: Additional information

#### 3. FAQ Section (AI Citation Optimized)
### Q: Question 1?
**A:** Direct answer

### Q: Question 2?
**A:** Direct answer

#### 4. Conclusion
- Key summary
- Additional resource links
- Call to action (CTA)

#### SEO Checklist
- Title length: __/60 chars [OK]
- Meta description: 150-160 chars suggestion
- Keyword density: 1-2% natural placement
- H2/H3 structure: Included [OK]
- Bullet points: Used [OK]
- Internal links: Identify opportunities

#### AI Search Exposure Tips
- FAQ Schema application recommended
- Structured data (JSON-LD) suggestion
- Source citation method
- Citation-friendly format (specific numbers, examples)
"""
    return prompt


def create_analysis_prompt(generated_content: str, seo_rules: str, ai_rules: str) -> str:
    """
    분석 프롬프트 생성

    Args:
        generated_content: 생성된 콘텐츠
        seo_rules: SEO 규칙
        ai_rules: AI 검색 규칙

    Returns:
        생성된 분석 프롬프트
    """
    # SEO 규칙 처리
    seo_summary = seo_rules[:1500] if seo_rules and len(seo_rules) > 1500 else (seo_rules if seo_rules else "기본: 제목 60자 이내, 클릭 유도, 핵심 키워드 포함")

    # AI 규칙 처리
    ai_summary = ai_rules[:1500] if ai_rules and len(ai_rules) > 1500 else (ai_rules if ai_rules else "기본: 직접적인 답변 제공, 구조화된 정보, 출처 표기")

    prompt = f"""당신은 SEO 및 AI 검색 노출 평가 전문가입니다.

다음 생성된 콘텐츠를 평가해주세요.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[생성된 콘텐츠]
{generated_content}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[SEO 규칙 요약]
{seo_summary}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[AI 검색 규칙 요약]
{ai_summary}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 평가 기준

### 제목 평가 (50점)
1. 길이 (0-10): 50-60자면 만점
2. 키워드 배치 (0-10): 메인 키워드 포함 여부
3. 클릭 유도력 (0-10): 독자의 클릭을 유도하는 요소
4. AI 인용 가능성 (0-10): 구체적이고 인용 가능한 형태
5. 제목 다양성 (0-10): 5개 제목이 다양한 각도로 구성되었는지

### 본문 평가 (50점)
1. 구조화 (0-10): H2/H3, 불릿 포인트, 표 활용
2. E-E-A-T 요소 (0-10): 경험, 전문성, 권위성, 신뢰성
3. AI 친화적 형식 (0-10): FAQ, 직접적인 답변 형식
4. 키워드 최적화 (0-10): 자연스러운 배치
5. 이중 언어 지원 (0-10): 한국어/영어 버전 포함

## PASS/FAIL 기준
- PASS: 총점 70점 이상 AND 제목 35점 이상 AND 본문 35점 이상
- FAIL: 그 외

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

아래 형식에 맞춰 결과를 출력해주세요:

[평가 결과]
PASS / FAIL

[총점]
__/100

[제목 점수]
__/50
- 길이: _/10
- 키워드 배치: _/10
- 클릭 유도력: _/10
- AI 인용 가능성: _/10
- 제목 다양성: _/10

[본문 점수]
__/50
- 구조화: _/10
- E-E-A-T 요소: _/10
- AI 친화적 형식: _/10
- 키워드 최적화: _/10
- 이중 언어 지원: _/10

{{FAIL인 경우 아래 추가}}
[개선 피드백]
1. 제목 개선 사항:
   - 구체적인 개선 사항
2. 본문 개선 사항:
   - 구체적인 개선 사항
"""
    return prompt


def parse_analysis_result(analysis_text: str) -> Dict:
    """
    분석 결과 파싱 (PASS/FAIL + 피드백 추출)

    Args:
        analysis_text: 분석 결과 텍스트

    Returns:
        분석 결과 딕셔너리 {result, total_score, title_score, content_score, feedback}
    """
    result = {
        "result": "FAIL",
        "total_score": 0,
        "title_score": 0,
        "content_score": 0,
        "feedback": ""
    }

    # 평가 결과 추출 (PASS/FAIL)
    pass_match = re.search(r'\[평가 결과\]\s*(PASS|FAIL)', analysis_text)
    if pass_match:
        result["result"] = pass_match.group(1)

    # 총점 추출
    total_match = re.search(r'\[총점\]\s*(\d+)/100', analysis_text)
    if total_match:
        result["total_score"] = int(total_match.group(1))

    # 제목 점수 추출
    title_match = re.search(r'\[제목 점수\]\s*(\d+)/50', analysis_text)
    if title_match:
        result["title_score"] = int(title_match.group(1))

    # 본문 점수 추출
    content_match = re.search(r'\[본문 점수\]\s*(\d+)/50', analysis_text)
    if content_match:
        result["content_score"] = int(content_match.group(1))

    # 피드백 추출
    feedback_match = re.search(r'\[개선 피드백\](.*?)(?=\n\n|\Z)', analysis_text, re.DOTALL)
    if feedback_match:
        result["feedback"] = feedback_match.group(1).strip()

    return result


def generate_output_with_retry(api_key: str, input_content: str, seo_rules: str, ai_rules: str, max_retries: int = 3) -> Tuple[Optional[str], Dict]:
    """
    피드백 루프를 포함한 콘텐츠 생성 (최대 3회 재시도)

    Args:
        api_key: API Key
        input_content: 입력 콘텐츠
        seo_rules: SEO 규칙
        ai_rules: AI 검색 규칙
        max_retries: 최대 재시도 횟수

    Returns:
        (생성된 콘텐츠, 최종 분석 결과)
    """
    previous_feedback = ""
    final_content = None
    final_analysis = {"result": "FAIL", "total_score": 0, "title_score": 0, "content_score": 0, "attempts": 0}

    for attempt in range(1, max_retries + 1):
        print_info(f"생성 시도 {attempt}/{max_retries}...")

        # 콘텐츠 생성
        generation_prompt = create_generation_prompt(input_content, seo_rules, ai_rules, previous_feedback)
        content = call_api(api_key, generation_prompt)

        if not content:
            print_error(f"콘텐츠 생성 실패 (시도 {attempt})")
            if attempt == max_retries:
                return None, final_analysis
            continue

        # 분석 수행
        print_info("검색 랭킹 분석 중...")
        analysis_prompt = create_analysis_prompt(content, seo_rules, ai_rules)
        analysis_result = call_api(api_key, analysis_prompt)

        if not analysis_result:
            print_warning("분석 실패, 콘텐츠 사용 중...")
            final_content = content
            final_analysis["attempts"] = attempt
            break

        # 분석 결과 파싱
        parsed = parse_analysis_result(analysis_result)
        parsed["attempts"] = attempt

        print_info(f"분석 결과: {parsed['result']} | 총점: {parsed['total_score']}/100")
        print_info(f"  - 제목: {parsed['title_score']}/50")
        print_info(f"  - 본문: {parsed['content_score']}/50")

        # PASS 조건 확인
        if (parsed["result"] == "PASS" or
            (parsed["total_score"] >= ANALYSIS_PASS_THRESHOLD and
             parsed["title_score"] >= TITLE_PASS_THRESHOLD and
             parsed["content_score"] >= CONTENT_PASS_THRESHOLD)):
            print_success("콘텐츠 품질 검증 통과!")
            final_content = content
            final_analysis = parsed
            break
        elif attempt < max_retries:
            print_warning("품질 미달, 피드백 반영 후 재생성...")
            previous_feedback = parsed.get("feedback", "콘텐츠 품질 개선 필요")
        else:
            print_warning(f"최대 {max_retries}회 시도 완료, 마지막 결과 사용 중...")
            final_content = content
            final_analysis = parsed

    return final_content, final_analysis


def preprocess_input(api_key: str) -> bool:
    """
    입력 전처리: input_plan/CLAUDE.md가 있으면 input.txt 자동 생성

    Args:
        api_key: API Key

    Returns:
        input.txt가 수정되었는지 여부
    """
    input_plan_path = os.path.join(CURRENT_DIR, "input_plan", "CLAUDE.md")
    input_path = os.path.join(CURRENT_DIR, "input", "input.txt")

    # input_plan/CLAUDE.md 파일 존재 여부 확인
    if not os.path.exists(input_plan_path):
        print_info("input_plan/CLAUDE.md 파일이 없습니다. 기존 input.txt를 사용합니다.")
        return False

    print("\n0. 입력 전처리 (input_plan/CLAUDE.md 분석)...")
    print_info("input_plan/CLAUDE.md 파일을 발견했습니다.")

    # CLAUDE.md 내용 읽기
    claude_md_content = read_file(input_plan_path)
    if not claude_md_content:
        print_error("input_plan/CLAUDE.md 읽기 실패. 기존 input.txt를 사용합니다.")
        return False

    print_info("CLAUDE.md 분석 중...")

    # 웹서비스 여부 판단 (키워드 기반)
    web_service_keywords = ['웹서비스', 'web service', '웹 앱', 'web app', '사이트', 'website',
                          'api', '도구', 'tool', '플랫폼', 'platform', '서비스', 'service']
    is_web_service = any(keyword in claude_md_content.lower() for keyword in web_service_keywords)

    if is_web_service:
        print_info("웹서비스 프로젝트로 판단됨")
    else:
        print_info("블로그 글/튜토리얼 프로젝트로 판단됨")

    # blogger-doc-generator 에이전트를 통해 input.txt 생성
    # (실제로는 API를 호출하여 프롬프트 생성)
    article_type = "웹서비스 소개" if is_web_service else "블로그 글 작성 가이드"
    title_type = "서비스 소개형/기능 강조형/가치 제안형" if is_web_service else "사용법 설명형/팁 공유형/가이드형"

    preprocessor_prompt = f"""당신은 Blogger 콘텐츠 생성 전문가입니다.

다음 CLAUDE.md 파일 내용을 분석하여, SEO 최적화된 {article_type}를 위한 input.txt 내용을 생성해주세요.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[분석 결과]
프로젝트 유형: {article_type}
제목 타입 가이드: {title_type}

[CLAUDE.md 내용]
{claude_md_content[:10000]}  # 내용이 길 경우 앞부분 10000자만 사용

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

요구사항:
1. CLAUDE.md의 내용을 분석하여 프로젝트의 핵심 내용 파악
2. {article_type}을 위한 적절한 input.txt 형식으로 변환
3. 글의 주제, 타겟 독자, 핵심 전달 내용, 추가 요구사항 포함

{'웹서비스일 경우 제목 가이드:' if is_web_service else ''}
- 서비스 이름 + 핵심 기능 (예: "무료 도구: 저항값만 입력하면 Mouser 부품 자동 매칭")
- "도구", "서비스", "플랫폼" 등의 키워드 포함
- 사용법 설명("~하는 법")보다는 서비스 소개형
{'블로그 글일 경우 제목 가이드:' if not is_web_service else ''}
- "~하는 법", "~방법", "~가이드" 등 사용법 설명형
- 팁, 트릭, 해결책 강조

아래 형식에 맞춰 결과를 출력해주세요:

글의 주제: [CLAUDE.md에서 파악한 프로젝트 주제]
타겟 독자: [CLAUDE.md에서 파악한 타겟 독자]
핵심 전달 내용: [CLAUDE.md에서 파악한 핵심 전달 내용]
추가 요구사항: 프로젝트 유형을 고려하여 제목 생성 가이드 추가 ({article_type}에 맞는 제목 형태 제안)

이 내용은 input.txt 파일로 저장될 것입니다.
"""

    # API 호출
    generated_input = call_api(api_key, preprocessor_prompt)
    if not generated_input:
        print_error("input.txt 생성 실패. 기존 input.txt를 사용합니다.")
        return False

    # 생성된 input.txt 내용 정제
    # API 응답에서 필요한 부분만 추출
    import re
    input_content = generated_input

    # 필요한 형식으로 정제
    lines = input_content.split('\n')
    refined_lines = []
    for line in lines:
        if line.strip().startswith(('글의 주제:', '타겟 독자:', '핵심 전달 내용:', '추가 요구사항:')):
            refined_lines.append(line)
        elif line.strip() and refined_lines:
            refined_lines[-1] += '\n' + line

    refined_content = '\n'.join(refined_lines) if refined_lines else generated_input

    # input.txt 저장
    if write_file(input_path, refined_content):
        print_success("input.txt 자동 생성 완료 (input_plan/CLAUDE.md 기반)")
        return True

    return False


def run_optimization():
    """최적화 실행 메인 함수"""
    print_header("SEO Blog AI Optimizer v2.0.0")

    # 0. 의존성 확인
    print("\n0. 의존성 확인...")
    if not check_dependencies():
        print_error("anthropic 라이브러리가 설치되지 않았습니다.")
        print_info("설치 명령: pip install anthropic")
        input("\n엔터를 눌러 종료...")
        return

    print_success("의존성 확인 완료")

    # 1. API Key 읽기 (입력 전처리를 위해 먼저 읽음)
    print("\n1. API 설정 확인...")
    api_key_path = os.path.join(CURRENT_DIR, "config", "api_key.txt")
    api_key_content = read_file(api_key_path)

    if not api_key_content:
        print_error("API Key 파일을 찾을 수 없습니다.")
        print_info(f"파일 위치: {api_key_path}")
        input("\n엔터를 눌러 종료...")
        return

    api_key = extract_api_key(api_key_content)
    if not api_key:
        print_error("API Key를 찾을 수 없습니다.")
        print_info("config/api_key.txt를 확인해주세요.")
        print_info("형식: [your_api_key_here]")
        input("\n엔터를 눌러 종료...")
        return

    print_success("API Key 확인 완료")

    # 2. 입력 전처리 (input_plan/CLAUDE.md가 있으면 input.txt 자동 생성)
    preprocess_input(api_key)

    # 3. 입력 파일 읽기
    print("\n3. 입력 파일 읽기...")
    input_path = os.path.join(CURRENT_DIR, "input", "input.txt")
    input_content = read_file(input_path)

    if not input_content:
        print_error("input.txt 파일이 비어있거나 없습니다.")
        print_info(f"파일 위치: {input_path}")
        input("\n엔터를 눌러 종료...")
        return

    print_success(f"입력 파일 확인 완료 ({len(input_content)}자)")

    # 4. SEO 규칙 파일 읽기
    print("\n4. SEO 규칙 읽기...")
    seo_rules_path = os.path.join(CURRENT_DIR, "docs", "seo_rules.md")
    seo_rules = read_file(seo_rules_path)

    if not seo_rules:
        print_warning("SEO 규칙 파일이 비어있거나 없습니다. 기본 규칙 사용.")
    else:
        print_success("SEO 규칙 로드 완료")

    # 5. AI 검색 규칙 파일 읽기
    print("\n5. AI 검색 규칙 읽기...")
    ai_rules_path = os.path.join(CURRENT_DIR, "docs", "ai_search_rules.md")
    ai_rules = read_file(ai_rules_path)

    if not ai_rules:
        print_warning("AI 검색 규칙 파일이 비어있거나 없습니다. 기본 규칙 사용.")
    else:
        print_success("AI 검색 규칙 로드 완료")

    # 6. 피드백 루프를 포함한 콘텐츠 생성
    print("\n6. AI 콘텐츠 생성 및 검증...")

    result, analysis = generate_output_with_retry(api_key, input_content, seo_rules, ai_rules, MAX_RETRIES)

    if not result:
        input("\n엔터를 눌러 종료...")
        return

    # 7. 결과 저장
    print("\n6. 결과 저장...")
    output_path = os.path.join(CURRENT_DIR, "output", "output.txt")

    # 결과 헤더 추가 (생성 시도 정보, 최종 점수 포함)
    result_with_header = f"""# SEO 최적화 블로그 글 가이드

생성일시: {time.strftime('%Y-%m-%d %H:%M:%S')}
생성 시도: {analysis.get('attempts', 1)}/{MAX_RETRIES} {"(피드백 반영 후 재생성)" if analysis.get('attempts', 1) > 1 else ""}
최종 점수: {analysis.get('total_score', 0)}/100
  - 제목: {analysis.get('title_score', 0)}/50
  - 본문: {analysis.get('content_score', 0)}/50
검증 결과: {analysis.get('result', 'UNKNOWN')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{result}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

이 가이드는 SEO Blog AI Optimizer v2.0.0에 의해 생성되었습니다.
"""

    if write_file(output_path, result_with_header):
        print_info(f"총 글자 수: {len(result)}자")

    # 완료 메시지
    print_header("완료!")
    print_success("최적화가 성공적으로 완료되었습니다.")
    print_info(f"결과 파일: {output_path}")
    print()
    print("다음 단계:")
    print("  1. output/output.txt를 열어 결과 확인")
    print("  2. 가이드를 바탕으로 블로그 글 작성")
    print("  3. 게시 후 검색 노출 모니터링")
    print()


if __name__ == "__main__":
    try:
        run_optimization()
        # 터미널 환경이 아닌 경우 input() 스킵
        if sys.stdin.isatty():
            try:
                input("엔터를 눌러 종료...")
            except (EOFError, OSError):
                pass
    except KeyboardInterrupt:
        print("\n\n사용자가 중단했습니다.")
        sys.exit(0)
    except Exception as e:
        print_error(f"예상치 못한 오류: {e}")
        if sys.stdin.isatty():
            try:
                input("엔터를 눌러 종료...")
            except (EOFError, OSError):
                pass
        sys.exit(1)
