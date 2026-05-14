# CLAUDE.md — IndPenSim AI Research

이 파일은 Claude Code가 다음 세션에서 프로젝트 컨텍스트를 빠르게 파악하기 위한 문서입니다.

---

## 프로젝트 개요

- **목적**: 석사 논문 작성을 위한 연구 저장소
- **주제**: IndPenSim(Industrial Penicillin Simulation) 데이터셋을 활용한 바이오제약 배치 공정 AI 연구
- **언어**: Python (Google Colab 환경)

---

## 데이터셋 정보

### 파일 위치
- `data/raw/100_Batches_IndPenSim_V3.csv` — 메인 시계열 데이터 (~2.4 GB, 113,935행)
- `data/raw/100_Batches_IndPenSim_Statistics.csv` — 배치별 요약 통계 (100행)

> raw 데이터는 `.gitignore`에 의해 git 추적에서 제외됨. 원본 다운로드: http://www.industrialpenicillinsimulation.com/

### 데이터 구조 (V3 CSV)
- **전체 컬럼 수**: 2,239개
- **공정 변수** (39개): 시간, 폭기율, 교반 RPM, pH, 온도, DO, 페니실린 농도, 부피, 기질 농도 등
- **라만 분광 데이터** (2,200채널): 웨이브넘버 201 ~ 2400 cm⁻¹
- **실제 컬럼명** (코드 작성 시 반드시 사용):
  - 배치 ID: `Batch reference(Batch_ref:Batch ref)`
  - 통계 CSV 배치 ID: `Batch ref`
  - Fault 레이블: `Fault ref(0-NoFault 1-Fault)`
  - 라만 기록 여부: `2-PAT control(PAT_ref:PAT ref)`

### EDA 결과 (2026-05-14 확인)

| 항목 | 수치 |
|------|------|
| 총 배치 수 | 100 (Fault 10개 / Normal 90개) |
| 전체 행 수 | 113,935 |
| 공정 변수 수 | 39 |
| 라만 채널 수 | 2,200 (201~2400 cm⁻¹) |
| **라만 기록 비율** | **1.0%** (배치당 약 11~12회만 측정) |
| 수율 평균 | 3,029,064 kg |
| 수율 표준편차 | 750,817 kg (CV ≈ 24.8%) |

> **라만 1% 주의**: 라만 데이터는 극히 희소함. 소프트 센서 연구 시 학습 데이터 부족 문제 고려 필요.

---

## 현재 상태 (2026-05-14 기준)

- [x] 데이터 파일 확보
- [x] README.md 초안 작성
- [x] REVIEW.md 작성 (프로젝트 리뷰 및 개선사항)
- [x] `notebooks/00_overview.ipynb` EDA 코드 작성 완료
- [x] EDA 실행 완료 (Google Colab)
- [ ] 연구 주제 미확정 (후보 검토 중)
- [ ] 폴더 구조 미생성 (`src/`, `configs/`, `experiments/`, `results/`)
- [ ] 모델 코드 없음

---

## 연구 주제 후보 및 검토 의견

EDA 결과(특히 라만 기록 비율 1%)를 반영한 업데이트된 추천 순위:

### 1순위 — 딥러닝 기반 이상 감지 (Fault Detection)
- 공정 변수 39개 기반, 라만 데이터 불필요
- Fault 레이블 명확 (10 vs 90배치)
- 기준선: MSPC/PCA → 비교: LSTM-AE, Transformer-AE
- 평가 지표(AUROC, F1) 명확

### 2순위 — 배치 초기 데이터 기반 수율 예측 (Yield Prediction)
- 수율 CV 24.8%로 변동이 크므로 실용적 가치 높음
- 배치 초반 데이터로 최종 수율 조기 예측
- LSTM / Temporal Attention 모델 활용

### 3순위 — 라만 분광 기반 소프트 센서 (Soft Sensor)
- 라만이 1%만 기록 → 희소 데이터 처리가 논문 기여점이 될 수 있음
- 학습 데이터 부족 문제를 어떻게 해결하느냐가 핵심

---

## 주요 주의 사항

- **README 내용 무시**: README의 실험 계획(`pca_config.yaml` 등)은 미구현 상태. 데이터 기반으로 주제 도출 중
- **Colab matplotlib 한글 미지원**: 그래프 제목·축 레이블은 영문, 마크다운·print문은 한글 사용
- **컬럼명 주의**: CSV 컬럼명이 길고 복잡함. 노트북 상단 상수로 정의해 사용할 것

---

## 다음 세션 우선 과제

1. 연구 주제 최종 확정
2. 확정된 주제에 맞는 폴더 구조 생성 (`src/`, `experiments/` 등)
3. 전처리 코드 작성 (`src/preprocessing.py`)
