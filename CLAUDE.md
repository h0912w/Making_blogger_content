# SEO Blog AI Optimizer

SEO와 AI 검색 노출 관점에서 블로그 글과 제목을 최적화하는 도구

---

## 빠른 시작

### 1. 필수 라이브러리 설치
```bash
pip install anthropic
```

### 2. API Key 설정
`config/api_key.txt`에 GLM-5 API Key를 입력

### 3. 입력 파일 작성
`input/input.txt`에 글 설명 작성

### 4. 실행
- **Windows**: `run.bat` 더블클릭
- **터미널**: `python run.py`

### 5. 결과 확인
`output/output.txt`에서 결과 확인

---

## 특징

- ✅ 2026년 최신 SEO 트렌드 반영
- ✅ AI 검색 엔진(Perplexity, ChatGPT, SGE) 최적화
- ✅ E-E-A-T 기반 콘텐츠 가이드
- ✅ 구조화된 데이터(Schema) 예시
- ✅ FAQ 섹션 포함 (AI 인용 최적화)
- ✅ 더블클릭으로 실행 가능
- ✅ input_plan 폴더로 다른 프로젝트 CLAUDE.md 복사 시 input.txt 자동 생성

---

## 프로젝트 구조

```
ai-seo/
├── input/
│   └── input.txt          # 입력: 글 설명
├── input_plan/
│   └── CLAUDE.md         # (선택) 다른 프로젝트 CLAUDE.md 복사 → input.txt 자동 생성
├── output/
│   └── output.txt         # 출력: 최적화 결과
├── docs/
│   ├── seo_rules.md      # SEO 규칙 문서
│   ├── ai_search_rules.md # AI 검색 노출 규칙
│   └── validation_report.md # 검증 보고서
├── config/
│   └── api_key.txt       # GLM-5 API Key
├── agents/               # 서브에이전트 정의
│   ├── seo_researcher.md      # SEO 규칙 조사 에이전트
│   ├── ai_search_researcher.md # AI 검색 노출 조사 에이전트
│   ├── validator.md           # 검증 에이전트
│   ├── content_generator.md   # 콘텐츠 생성 에이전트
│   ├── search_ranking_analyzer.md # 검색 랭킹 분석 에이전트
│   └── tester.md             # QA 및 테스트 에이전트
├── run.py               # Python 실행 스크립트
├── run.bat              # Windows 실행 파일
├── requirements.txt      # 필수 라이브러리
└── CLAUDE.md            # 프로젝트 문서
```

---

## 에이전트 팀 구성

프로젝트에서 사용할 에이전트와 실제 에이전트 이름 매핑:

| # | 역할 | 에이전트 ID | 대응 파일 |
|---|--------|-------------|-----------|
| 0 | 입력 전처리 | `blogger-doc-generator` | (system) |
| 1 | SEO 규칙 조사 | `seo-rules-documenter` | agents/seo_researcher.md |
| 2 | AI 검색 최적화 | `ai-search-optimizer` | agents/ai_search_researcher.md |
| 3 | 검증 | `seo-search-verifier` | agents/validator.md |
| 4 | 콘텐츠 생성 | `blog-title-optimizer` | agents/content_generator.md |
| 5 | 검색 랭킹 분석 | `search-ranking-analyzer` | agents/search_ranking_analyzer.md |
| 6 | QA 및 테스트 | `qa-tester` | agents/tester.md |

---

## 에이전트 상세 설명

### 에이전트 0: input-preprocessor (입력 전처리)

- **에이전트 ID**: `blogger-doc-generator`
- **역할**: input_plan 폴더에 있는 CLAUDE.md를 해석하여 적절한 input.txt를 자동 생성/수정
- **작업**:
  1. `input_plan/CLAUDE.md` 파일 존재 여부 확인
  2. **파일 존재 시**:
     - `blogger-doc-generator` 에이전트를 호출하여 CLAUDE.md 분석
     - 프로젝트 내용을 기반으로 `input.txt` 생성
     - 생성된 input.txt에는 글의 주제, 타겟 독자, 핵심 전달 내용, 추가 요구사항 포함
  3. **파일 미존재 시**:
     - 기존 `input.txt`를 그대로 유지 (수정하지 않음)
  4. **키워드 분석 (추가)**:
     - input.txt를 바탕으로 구글 검색이나 AI 추천에 낫을 하기 쉬운 키워드를 분석
     - 각 키워드별 구글 월간 검색량, 경쟁도, 기존 상위 글 수 조사
     - 낫은 하기 쉬운 키워드(검색량 높고 경쟁도 낮은 키워드)를 추천
     - 제목 생성 시 추천 키워드 3개를 꼭 포함하도록 제한
  5. 후속 에이전트들에게 처리 완료 신호 전달
- **실행 타이밍**: 프로젝트 실행 시 가장 먼저 실행
- **API**: GLM-5 API 사용

### 에이전트 1: seo-rules-documenter (SEO 규칙 조사)

- **에이전트 ID**: `seo-rules-documenter`
- **역할**: SEO 관점에서 준수해야 하는 규칙 조사 및 문서화
- **작업**: `docs/seo_rules.md` 생성 및 관리
- **실행 타이밍**: 프로젝트 실행 시마다 최신 경향 파악 후 문서 최신화
- **검색 대상**:
  - 최신 SEO 트렌드 (2026)
  - 구글 검색 알고리즘 업데이트
  - 제목, 메타디스크립션, 본문 최적화 규칙
  - 키워드 배치, 내부 링크, 이미지 SEO

### 에이전트 2: ai-search-optimizer (AI 검색 최적화)

- **에이전트 ID**: `ai-search-optimizer`
- **역할**: ChatGPT, Gemini 등 AI가 사이트/콘텐츠를 추천할 수 있는 규칙 조사
- **작업**: `docs/ai_search_rules.md` 생성 및 관리
- **실행 타이밍**: 프로젝트 실행 시마다 최신화
- **검색 대상**:
  - AI 검색 엔진(Perplexity, ChatGPT Search 등) 동작 원리
  - AI가 신뢰하는 소스 특성
  - E-E-A-T(경험, 전문성, 권위성, 신뢰성) 요구사항
  - 구조화된 데이터, FAQ 포맷, 직접적인 답변 구조

### 에이전트 3: seo-search-verifier (검증)

- **에이전트 ID**: `seo-search-verifier`
- **역할**: 1, 2번 에이전트가 만든 문서 더블체크
- **작업**:
  1. `docs/seo_rules.md` 검증
  2. `docs/ai_search_rules.md` 검증
  3. `docs/validation_report.md` 생성
  4. 문제 발견 시 피드백 전달 → 1, 2번 에이전트 재작업
- **검증 항목**:
  - 규칙 간 충돌 여부
  - 최신성 (2026년 트렌드 반영 여부)
  - 실현 가능성
  - 구체적이고 실행 가능한 가이드인지

### 에이전트 4: blog-title-optimizer (콘텐츠 생성)

- **에이전트 ID**: `blog-title-optimizer`
- **역할**: 완성된 문서 기반으로 5개의 제목 추천 및 한/영 본문 가이드 생성
- **작업**:
  1. `input/` 폴더의 글 설명 파일 읽기
  2. `docs/seo_rules.md`, `docs/ai_search_rules.md` 참조
  3. 5개의 제목 추천 (예상 클릭률, SEO 점수, 설명 포함)
  4. 한국어와 영어 두 버전의 본문 가이드 생성
  5. 피드백 루프를 통한 품질 개선 (최대 3회)
  6. 결과를 `output/` 폴더에 txt 파일로 저장
- **API**: GLM-5 API 사용

### 에이전트 5: search-ranking-analyzer (검색 랭킹 분석)

- **에이전트 ID**: `search-ranking-analyzer`
- **역할**: 생성된 콘텐츠가 구글 검색 노출과 AI 추천에 적합한지 평가 및 키워드 성공 가능성 분석
- **작업**:
  1. 생성된 콘텐츠 분석
  2. 제목 평가 (50점): 길이, 키워드 배치, 클릭 유도력, AI 인용 가능성, 다양성
  3. 본문 평가 (50점): 구조화, E-E-A-T 요소, AI 친화적 형식, 키워드 최적화, 이중 언어 지원
  4. **키워드 성공 가능성 분석 (추가)**:
     - 제목과 본문에서 핵심 키워드 추출 (최대 5개)
     - 각 키워드별 구글 월간 검색량 조사
     - 각 키워드별 경쟁 콘텐츠 수 조사
     - 키워드 난이도(상/중/하) 평가
     - 경쟁 강도 분석 (높음/보통/낮음)
     - 성공 가능성 점수 (0-100): 검색량 × (1/경쟁도) × 콘텐츠 품질점수
     - 추천 타겟 키워드 선정 (성공 가능성 상위 3개)
  5. PASS/FAIL 판정 (총점 70점 이상 AND 제목 35점 이상 AND 본문 35점 이상 AND 성공 가능성 점수 50점 이상)
  6. FAIL 시 구체적인 피드백 및 키워드 최적화 제안 제공
- **API**: GLM-5 API 사용
- **출력 추가 항목**:
  - 키워드별 검색량 표
  - 경쟁 콘텐츠 수 표
  - 성공 가능성 순위
  - 추천 타겟 키워드 리스트

### 에이전트 6: qa-tester (QA 및 테스트)

- **에이전트 ID**: `qa-tester`
- **역할**: 모든 코딩 작업 후 기능 테스트 및 QA
- **작업**:
  1. 코드 리뷰 및 테스트 수행
  2. 기능 동작 확인 (run.py, run.bat, 워크플로우)
  3. 문제 발견 시 구체적 피드백 전달 → 코딩 에이전트 수정
  4. 재테스트 후 최종 승인
- **테스트 대상**:
  - 파일 읽기/쓰기 기능
  - API Key 추출 기능
  - API 호출 기능
  - 에러 처리 기능
  - Windows 호환성

---

## 워크플로우

```
프로젝트 실행
    ↓
에이전트 0: 입력 전처리 → input.txt 생성/수정 (blogger-doc-generator)
    ↓ (input_plan/CLAUDE.md 존재 시: 자동 생성, 미존재 시: 기존 input.txt 유지)
에이전트 1: SEO 규칙 조사 → docs/seo_rules.md (seo-rules-documenter)
에이전트 2: AI 검색 규칙 조사 → docs/ai_search_rules.md (ai-search-optimizer)
    ↓
에이전트 3: 검증 → docs/validation_report.md (seo-search-verifier)
    ↓ (문제 있으면 1, 2로 피드백 루프)
에이전트 4: 콘텐츠 생성 (제목 5개 + 한/영 버전) (blog-title-optimizer)
    ↓
에이전트 5: 검색 랭킹 분석 (search-ranking-analyzer)
    ↓ (FAIL이면 피드백 반영 후 에이전트 4 재시도, 최대 3회)
에이전트 6: 테스트 및 QA → 기능 검증 (qa-tester)
    ↓ (문제 있으면 코딩 에이전트로 피드백 → 재테스트)
최종 승인
```

---

## 입력 포맷 (input/)

### 파일명
`input.txt`

### 파일 내용 형식

```
글의 주제: 파이썬으로 웹 스크래핑 시작하기
타겟 독자: 프로그래밍 입문자, 웹 개발 관심 있는 사람
핵심 전달 내용: 파이썬 스크래핑 기초, 필수 라이브러리, 실전 예제
추가 요구사항: 코드 예시 포함, 에러 처리 방법 설명
```

---

## 출력 포맷 (output/)

### 파일명
`output.txt`

### 출력 내용

```
# SEO 최적화 블로그 글 가이드

생성일시: 2026-03-07 14:30:45
생성 시도: 2/3 (피드백 반영 후 재생성)
최종 점수: 78/100
  - 제목: 40/50
  - 본문: 38/50
검증 결과: PASS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[한국어 버전]

=== 제목 추천 (5개) ===
1. [제목]
   - 예상 클릭률: High/Medium/Low
   - SEO 점수: 0-100
   - 설명: 간단한 설명
...

=== 본문 구성 가이드 ===
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[English Version]

=== Title Recommendations (5) ===
...

=== Body Content Guide ===
...
```

---

## 사용 방법

### input_plan 폴더 사용법 (선택)

다른 프로젝트에서 진행 중인 CLAUDE.md를 활용하여 자동으로 input.txt를 생성할 수 있습니다.

1. `input_plan/` 폴더에 다른 프로젝트의 `CLAUDE.md` 파일을 복사
2. `run.bat` 실행 시 자동으로 `input.txt`가 생성됨
3. `input_plan/CLAUDE.md`가 없으면 기존 `input.txt`를 사용

**input_plan 사용 예시:**
```
input_plan/
└── CLAUDE.md    # 다른 프로젝트에서 복사한 CLAUDE.md
```

---

### 방법 1: 더블클릭 실행 (가장 간단)

1. `input/input.txt`에 글 내용 작성
2. `run.bat` 더블클릭
3. `output/output.txt`에서 결과 확인

**최초 실행 전 필요한 작업:**
```bash
pip install anthropic
```

### 방법 2: Python으로 직접 실행

```bash
python run.py
```

### 방법 3: Claude Code에서 실행

프로젝트 폴더에서 `claude`를 실행하고 다음 요청:

```
input/input.txt에 있는 내용을 바탕으로 SEO 최적화된 블로그 글을 생성해줘.
docs/seo_rules.md와 docs/ai_search_rules.md를 참고해서 output/output.txt에 결과를 저장해줘.
```

### 방법 4: 각 에이전트 순차 실행 (Claude Code)

1. **에이전트 1 실행** - SEO 규칙 조사
   ```
   docs/seo_rules.md에 최신 SEO 규칙을 조사해서 문서화해줘.
   ```
   → `seo-rules-documenter` 에이전트가 자동으로 호출됨

2. **에이전트 2 실행** - AI 검색 노출 규칙 조사
   ```
   docs/ai_search_rules.md에 AI 검색 노출 규칙을 조사해서 문서화해줘.
   ```
   → `ai-search-optimizer` 에이전트가 자동으로 호출됨

3. **에이전트 3 실행** - 검증
   ```
   docs/seo_rules.md와 docs/ai_search_rules.md를 검증해서 docs/validation_report.md를 생성해줘.
   문제가 있으면 피드백 전달해서 수정해줘.
   ```
   → `seo-search-verifier` 에이전트가 자동으로 호출됨

4. **에이전트 4 실행** - 콘텐츠 생성
   ```
   input/input.txt를 읽고, docs/seo_rules.md와 docs/ai_search_rules.md를 참고해서
   최적화된 블로그 글 제목 5개와 본문 가이드(한국어/영어)를 output/output.txt에 저장해줘.
   config/api_key.txt의 GLM-5 API를 사용해.
   ```
   → `blog-title-optimizer` 에이전트가 자동으로 호출됨

5. **에이전트 5 실행** - 검색 랭킹 분석 (선택)
   ```
   output/output.txt에 있는 콘텐츠를 분석해서 구글 검색 노출과 AI 추천에 적합한지 평가해줘.
   docs/seo_rules.md와 docs/ai_search_rules.md를 참고해.
   ```
   → `search-ranking-analyzer` 에이전트가 자동으로 호출됨

6. **에이전트 6 실행** - 테스트 및 QA
   ```
   run.py와 run.bat의 기능을 테스트하고 QA를 수행해줘.
   ```
   → `qa-tester` 에이전트가 자동으로 호출됨

---

## 주의사항

- API Key는 공개 저장소에 커밋하지 마세요 (`.gitignore`에 포함됨)
- input.txt는 매번 내용을 변경하여 사용하세요
- output.txt는 실행할 때마다 덮어쓰입니다
- output 폴더는 깃허브에 업로드되므로 핸드폰에서도 결과를 확인할 수 있습니다
- input_plan 폴더에 CLAUDE.md를 넣으면 기존 input.txt가 자동으로 덮어씌워집니다 (주의 필요)
- **매번 run.bat 실행 후 깃허브에 푸시하세요:** `git add -A && git commit -m "Update SEO optimization result" && git push`

---

## 라이선스

MIT License
