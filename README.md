# SEO Blog AI Optimizer

SEO와 AI 검색 노출 관점에서 블로그 글과 제목을 최적화하는 도구

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

## 프로젝트 구조

```
ai-seo/
├── input/
│   └── input.txt          # 입력: 글 설명
├── output/
│   └── output.txt         # 출력: 최적화 결과
├── docs/
│   ├── seo_rules.md      # SEO 규칙 문서
│   ├── ai_search_rules.md # AI 검색 노출 규칙
│   └── validation_report.md # 검증 보고서
├── config/
│   └── api_key.txt       # GLM-5 API Key
├── agents/               # 서브에이전트 정의
├── run.py               # Python 실행 스크립트
├── run.bat              # Windows 실행 파일
├── requirements.txt      # 필수 라이브러리
├── CLAUDE.md            # 프로젝트 문서
└── README.md            # 이 파일
```

## 특징

- ✅ 2026년 최신 SEO 트렌드 반영
- ✅ AI 검색 엔진(Perplexity, ChatGPT, SGE) 최적화
- ✅ E-E-A-T 기반 콘텐츠 가이드
- ✅ 구조화된 데이터(Schema) 예시
- ✅ FAQ 섹션 포함 (AI 인용 최적화)
- ✅ 더블클릭으로 실행 가능

## 입력 예시

```
글의 주제: 파이썬으로 웹 스크래핑 시작하기
타겟 독자: 프로그래밍 입문자, 웹 개발 관심 있는 사람
핵심 전달 내용: 파이썬 스크래핑 기초, 필수 라이브러리, 실전 예제
추가 요구사항: 코드 예시 포함, 에러 처리 방법 설명
```

## 출력 예시

```
[제목] 6개월간 실전 테스트 후 내린 파이썬 웹 스크래핑 결론

[본문에 포함될 핵심 키워드]
- 파이썬 웹 스크래핑
- BeautifulSoup
- Requests

[본문 구성 가이드]
...

[SEO 점검 리스트]
...

[AI 검색 노출 팁]
...
```

## 주의사항

- API Key는 공개 저장소에 커밋하지 마세요
- input.txt는 매번 내용을 변경하여 사용하세요
- output.txt는 실행할 때마다 덮어쓰입니다

## 라이선스

MIT License
