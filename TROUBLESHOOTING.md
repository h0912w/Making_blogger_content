# 문제 해결 가이드 (Troubleshooting Guide)

이 문서는 SEO Blog AI Optimizer 프로젝트 사용 중 발생할 수 있는 문제와 그 해결 방안을 정리한 것입니다.

---

## 목차

1. [API 관련 문제](#api-관련-문제)
2. [파일 입출력 문제](#파일-입출력-문제)
3. [에이전트 실행 문제](#에이전트-실행-문제)
4. [Git 관련 문제](#git-관련-문제)
5. [Windows 환경 문제](#windows-환경-문제)

---

## API 관련 문제

### 문제 1: API Key 인증 실패
**증상:** ` anthropic.AuthenticationError` 또는 `401 Unauthorized` 오류 발생

**원인:**
- `config/api_key.txt` 파일이 없거나 빈 파일
- API Key가 만료되었거나 잘못됨

**해결 방법:**
1. `config/api_key.txt` 파일에 유효한 GLM-5 API Key 입력
2. API Key 앞뒤에 불필요한 공백이나 줄바꿈 제거
3. API Key가 정상인지 GLM-5 콘솔에서 확인

```bash
# API Key 확인
cat config/api_key.txt
```

---

### 문제 2: API 호출 시간 초과
**증상:** `anthic.APITimeoutError` 또는 응답 없음

**원인:**
- 네트워크 연결 불안정
- API 서버 일시적 장애
- 요청이 너무 큼

**해결 방법:**
1. 인터넷 연결 확인
2. 잠시 후 재시도
3. `run.py`에서 timeout 값 조정 (기본 120초)

---

## 파일 입출력 문제

### 문제 3: input.txt 파일을 찾을 수 없음
**증상:** `FileNotFoundError: input/input.txt not found`

**원인:**
- `input/` 폴더가 없음
- `input.txt` 파일이 존재하지 않음

**해결 방법:**
1. `input/` 폴더 생성
2. `input/input.txt` 파일 생성 후 내용 작성

```bash
# 폴더 및 파일 생성
mkdir -p input
echo "글의 주제와 목표" > input/input.txt
```

---

### 문제 4: output/ 폴더 생성 실패 (Windows)
**증상:** `OSError: [WinError 123]` 또는 경로 오류

**원인:**
- Windows에서 경로 구분자 사용 오류
- 권한 문제

**해결 방안 (적용됨):**
- `pathlib.Path` 사용으로 경로 처리 개선
- Windows 호환성 보장을 위해 `os.makedirs(exist_ok=True)` 사용

---

## 에이전트 실행 문제

### 문제 5: 에이전트가 응답하지 않음
**증상:** Agent 실행 후 응답 없음

**원인:**
- 프롬프트가 너무 복잡함
- 컨텍스트가 초과됨

**해결 방법:**
1. 간단한 요청으로 변경
2. 특정 에이전트만 개별 실행
3. `docs/` 폴더의 규칙 문서 크기 확인

---

### 문제 6: 검증 점수가 낮게 나옴
**증상:** 에이전트 5에서 FAIL 판정

**원인:**
- 제목이 너무 길거나 짧음
- 키워드 배치가 부적절함
- 본문 구조가 AI 친화적이지 않음

**해결 방법:**
1. 피드백 내용 확인
2. `docs/seo_rules.md`와 `docs/ai_search_rules.md` 참조하여 수정
3. 에이전트 4 재실행 (최대 3회 가능)

---

## Git 관련 문제

### 문제 7: 푸시 권한 거부
**증상:** `! [remote rejected] master -> master (permission denied)`

**원인:**
- 깃허브 설정에서 `git push` 명령어가 차단됨
- `.claude/settings.local.json`에 권한이 설정되지 않음

**해결 방안 (적용됨):**
```json
{
  "permissions": {
    "allowed": [
      "Bash(git push:*)"
    ]
  }
}
```

---

### 문제 8: LF/CRLF 줄바꿈 경고
**증상:** `LF will be replaced by CRLF` 경고

**원인:**
- Windows와 Git 간 줄바꿈 문자 방식 차이

**해결 방법:**
1. 경고는 정상이므로 무시 가능
2. 일관성을 위해 `.gitattributes` 설정 가능

```gitattributes
* text=auto
```

---

### 문제 9: 핸드폰 SSH 연결에서 git push 실패
**증상:** `could not read Username for 'https://github.com': No such file or address`

**원인:**
- 핸드폰에서 SSH 원격 접속 시 대화형 입력(`/dev/tty`)이 불가능
- HTTPS 방식은 브라우저 로그인이 필요함

**해결 방법:**
1. SSH 키 생성
```bash
ssh-keygen -t ed25519 -C "이메일주소@example.com" -f ~/.ssh/id_ed25519 -N ""
```

2. SSH 에이전트에 키 추가
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

3. 깃허브에 공개 키 등록
   - https://github.com/settings/keys 접속
   - `New SSH key` 클릭
   - `cat ~/.ssh/id_ed25519.pub` 내용 붙여넣기

4. Remote URL을 SSH로 변경
```bash
git remote set-url origin git@github.com:사용자명/저장소명.git
```

---

## Windows 환경 문제

### 문제 10: batch 파일 실행 시 encoding 오류
**증상:** `UnicodeDecodeError` 또는 한글 깨짐

**원인:**
- Windows 기본 인코딩(CP949)과 UTF-8 간 호환성 문제

**해결 방안 (적용됨):**
```python
# run.py 수정
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

---

### 문제 11: Python 모듈 설치 실패
**증상:** `ModuleNotFoundError: No module named 'anthropic'`

**원인:**
- 필요한 패키지가 설치되지 않음

**해결 방법:**
```bash
pip install anthropic
```

---

## 문제 보고

위 목록에 없는 문제가 발생하면 다음 정보를 포함하여 보고해주세요:

1. 사용 환경 (OS, Python 버전)
2. 에러 메시지 전체
3. 재현 단계
4. 관련 파일 (가능한 경우)

**이슈 트래커:** https://github.com/[사용자명]/ai-seo/issues

---

## 업데이트 이력

| 날짜 | 문제 | 상태 |
|------|------|------|
| 2026-03-08 | 핸드폰 SSH 연결 git push 문제 및 SSH 키 설정 가이드 추가 | 해결됨 |
| 2026-03-08 | git push 권한 문제 | 해결됨 |
| 2026-03-08 | Windows 경로 처리 개선 | 적용됨 |
| 2026-03-08 | 문서 생성 | 초기 버전 |
