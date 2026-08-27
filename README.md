# Apparel Operations AI Search API

의류 벤더 현장에서 반복적으로 발생하는 샘플·원단 자료 검색 문제를 구조화한 포트폴리오 프로젝트입니다. 합성 데이터 120건을 SQLite에 저장하고, FastAPI로 CRUD·필터·검색 API를 제공합니다. 검색은 한글 부분 일치에 유리한 문자 n-gram TF-IDF와 코사인 유사도를 사용합니다.

## 해결하려는 문제

- 자료 위치와 명칭이 일정하지 않아 검색 시간이 반복적으로 발생
- 바이어 요청, 검수 상태, 납기와 보관 위치를 한 번에 확인하기 어려움
- 정상 결과뿐 아니라 중복 등록, 짧은 검색어, 빈 데이터 같은 실패 조건 검증 필요

## 주요 기능

- 합성 의류 샘플 데이터 120건 자동 생성
- SQLite 저장 및 브랜드·상태 필터 조회
- Pydantic 기반 입력 검증과 중복 데이터 409 응답
- TF-IDF 기반 한글 유사 검색과 일치 필드 표시
- 검색 처리시간 측정
- Swagger UI 자동 문서화 (`/docs`)
- pytest API·검색 테스트
- Docker 및 docker-compose 실행 환경

## 기술 스택

`Python 3.12` `FastAPI` `Pydantic` `SQLite` `pandas` `scikit-learn` `pytest` `Docker`

## 실행

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m app.seed
uvicorn app.main:app --reload
```

- API 문서: http://127.0.0.1:8000/docs
- 상태 확인: http://127.0.0.1:8000/health

## API 예시

```bash
curl -X POST http://127.0.0.1:8000/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query":"네이비 재킷 검수","limit":3}'
```

## 테스트와 벤치마크

```bash
pytest -q
python scripts/benchmark.py
```

로컬 Windows/Python 3.12 환경 실측 결과:

- 자동화 테스트: **5개 전체 통과**
- 검색 대상: **합성 데이터 120건**
- 검색 실행: **100회**
- 평균 검색시간: **7.22ms**
- P95 검색시간: **7.70ms**
- 최대 검색시간: **9.62ms**

환경에 따라 결과는 달라질 수 있으며 `python scripts/benchmark.py`로 재측정할 수 있습니다.

## 데이터 및 보안

프로젝트의 데이터는 실제 회사·바이어 자료가 아닌 규칙 기반 합성 데이터입니다. 회사 정보, 고객정보, 실제 샘플 번호는 포함하지 않습니다.

## 구조

```text
app/
  main.py          # FastAPI 엔드포인트
  database.py      # SQLite 연결·스키마
  repository.py    # 데이터 접근 계층
  search.py        # TF-IDF 검색
  schemas.py       # Pydantic 모델
  seed.py          # 합성 데이터 생성
tests/             # API·검색 테스트
scripts/benchmark.py
```

## 향후 개선

- 임베딩 모델과 벡터 데이터베이스를 이용한 의미 검색 비교
- 사용자 인증과 역할별 접근 제어
- 검색 품질 평가 데이터셋 및 Recall@K 측정
- CI 파이프라인과 클라우드 배포

