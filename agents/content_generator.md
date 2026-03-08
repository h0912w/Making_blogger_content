# Content Generator Agent

## 역할
완성된 문서를 기반으로 적절한 제목과 본문 내용을 정리하여 txt 파일로 생성

## 작업 목표
- `input/` 폴더의 글 설명 파일 읽기
- `docs/seo_rules.md`, `docs/ai_search_rules.md` 참조
- 5개의 제목 추천 (각 제목에 예상 클릭률, SEO 점수, 설명 포함)
- 한국어와 영어 두 버전의 본문 가이드 생성
- 피드백 루프를 통한 품질 개선 (최대 3회)
- 결과를 `output/` 폴더에 txt 파일로 저장

## 사용 API
- GLM-5 API
- API Key: `config/api_key.txt`에서 읽기

## 작업 프로세스

```
1. input/input.txt 파일 읽기
   ↓
2. docs/seo_rules.md 참조
   ↓
3. docs/ai_search_rules.md 참조
   ↓
4. GLM-5 API를 활용해 최적화된 콘텐츠 생성 (제목 5개 + 한/영 버전)
   ↓
5. Search Ranking Analyzer가 콘텐츠 품질 평가
   ↓ (FAIL인 경우 피드백 반영 후 4단계 재시도, 최대 3회)
6. output/output.txt로 저장
```

## 입력 형식

input/input.txt 내용 예시:
```
글의 주제: 파이썬으로 웹 스크래핑 시작하기
타겟 독자: 프로그래밍 입문자, 웹 개발 관심 있는 사람
핵심 전달 내용: 파이썬 스크래핑 기초, 필수 라이브러리, 실전 예제
추가 요구사항: 코드 예시 포함, 에러 처리 방법 설명
```

## 생성할 콘텐츠 구조

### [한국어 버전]

#### === 제목 추천 (5개) ===
각 제목에 다음 정보 포함:
- 제목 (50-60자)
- 예상 클릭률: High/Medium/Low
- SEO 점수: 0-100
- 설명: 제목 선택 이유 및 특징

제목 유형 (5개를 다양하게 구성):
1. 질문형: "어떻게 X를 하는가?"
2. 숫자형: "X가지 방법으로 Y 달성하기"
3. 혜택형: "X를 위한 Y의 이점"
4. 궁금증형: "당신이 몰랐던 X의 비밀"
5. 긴급형: "지금 바로 시작해야 하는 X"

#### === 본문 구성 가이드 ===

##### 본문에 포함될 핵심 키워드
- 메인 키워드
- 관련 키워드 (LSI)
- 롱테일 키워드

##### 1. 도입부 (AI 검색 친화적)
- 직접적인 답변 제공
- 글의 목적 명확히
- 독자의 검색 의도 파악

##### 2. 본문 (SEO 최적화)
- H2, H3 섹션 구조
- 키워드 자연스럽게 배치
- 불릿 포인트 활용
- 코드 예시/이미지 포함

##### 3. FAQ 섹션 (AI 인용 최적화)
### Q: 질문?
**A:** 직접적인 답변

##### 4. 결론
- 핵심 요약
- 추가 리소스 링크
- 행동 유도 (CTA)

##### SEO 점검 리스트
- 제목 길이: __/60 자
- 메타디스크립션 포함 여부
- 키워드 밀도 확인
- 내부 링크 기회

##### AI 검색 노출 팁
- FAQ 섹션 추가 권장
- 구조화된 데이터 제안
- 출처 표기 방법

### [English Version]

#### === Title Recommendations (5) ===
Same structure as Korean version:
- Title (50-60 characters)
- Expected CTR: High/Medium/Low
- SEO Score: 0-100
- Description: Reason and characteristics

#### === Body Content Guide ===

##### Key Keywords to Include
- Main keyword
- Related keywords (LSI)
- Long-tail keywords

##### 1. Introduction (AI Search Friendly)
- Direct answer provided
- Clear purpose of the article
- Understand reader's search intent

##### 2. Body (SEO Optimized)
- H2, H3 section structure
- Natural keyword placement
- Bullet points usage
- Code examples/images included

##### 3. FAQ Section (AI Citation Optimized)
### Q: Question?
**A:** Direct answer

##### 4. Conclusion
- Key summary
- Additional resource links
- Call to action (CTA)

##### SEO Checklist
- Title length: __/60 chars
- Meta description included
- Keyword density check
- Internal link opportunities

##### AI Search Exposure Tips
- FAQ section recommended
- Structured data suggestion
- Source citation method

## GLM-5 API 호출 프롬프트 구조

```python
prompt = f"""
당신은 SEO 및 AI 검색 노출 전문가입니다.

다음 정보를 바탕으로 최적화된 블로그 글 제목 5개와 본문 가이드를 한국어와 영어로 생성해주세요.

[글 설명]
{input_content}

[SEO 규칙 요약]
{seo_rules}

[AI 검색 노출 규칙 요약]
{ai_rules}

[이전 피드백 반영]  # 재생성 시에만 추가
{previous_feedback}

요구사항:
1. 제목은 5개 제안하며, 각 제목에 예상 클릭률(High/Medium/Low), SEO 점수(0-100), 설명 포함
2. 5개의 제목은 다른 각도로 구성 (질문형, 숫자형, 혜택형, 궁금증형, 긴급형 등)
3. 본문은 한국어와 영어 두 버전으로 생성
4. 본문은 H2/H3 구조, 키워드 자연스러운 배치, 3-5문장 단락
5. AI 검색 엔진이 쉽게 인용할 수 있는 직접적인 답변 형식
6. E-E-A-T 요소 강화 (경험, 전문성, 권위성, 신뢰성)
7. 구조화된 정보 (불릿 포인트, 표, 번호 매기기) 활용
8. FAQ 섹션 포함 (AI 인용 최적화)

위 형식에 맞춰 결과를 출력해주세요.
"""
```

## 출력 파일 형식

output/output.txt에 저장:
```
# SEO 최적화 블로그 글 가이드

생성일시: 2026-03-07 14:30:45
생성 시도: 2/3 (피드백 반영 후 재생성)
최종 점수: 78/100
  - 제목: 40/50
  - 본문: 38/50
검증 결과: PASS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

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

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

이 가이드는 SEO Blog AI Optimizer v2.0.0에 의해 생성되었습니다.
```

## API 설정
```python
import os

API_KEY = open("config/api_key.txt").read().strip()
API_BASE_URL = "https://api.z.ai/api/anthropic"  # GLM-5 API endpoint
MAX_RETRIES = 3  # 최대 재시도 횟수
ANALYSIS_PASS_THRESHOLD = 70  # 총점 합격 기준
TITLE_PASS_THRESHOLD = 35  # 제목 점수 합격 기준
CONTENT_PASS_THRESHOLD = 35  # 본문 점수 합격 기준
```
