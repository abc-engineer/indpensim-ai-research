# CLAUDE.md — IndPenSim AI Research

이 파일은 Claude Code가 다음 세션에서 프로젝트 컨텍스트를 빠르게 파악하기 위한 문서입니다.

---

## 프로젝트 개요

- **목적**: 석사 논문 작성을 위한 연구 저장소
- **주제**: IndPenSim(Industrial Penicillin Simulation) 데이터셋을 활용한 바이오제약 배치 공정 AI 연구
- **언어**: Python

---

## 데이터셋 정보

### 파일 위치
- `data/raw/100_Batches_IndPenSim_V3.csv` — 메인 시계열 데이터 (~2.4 GB, ~113,936행)
- `data/raw/100_Batches_IndPenSim_Statistics.csv` — 배치별 요약 통계 (100행)

> raw 데이터는 `.gitignore`에 의해 git 추적에서 제외됨. 원본 다운로드: http://www.industrialpenicillinsimulation.com/

### 데이터 구조 (V3 CSV)
- **전체 컬럼 수**: 2,239개
- **공정 변수** (39개): 시간, 폭기율, 교반 RPM, pH, 온도, DO, 페니실린 농도, 부피, 기질 농도 등
- **라만 분광 데이터** (2,200개 채널): 웨이브넘버 201 ~ 2400
- **주요 메타 컬럼**: `Batch_ref`, `Fault_ref`, `Fault flag`, `Control_ref`, `PAT_ref`

### 배치 통계 (Statistics CSV)
- **총 배치 수**: 100
- **Fault 배치**: 10개 (10%)
- **No-Fault 배치**: 90개 (90%)
- **페니실린 수율** (Penicillin_yield_total): 평균 약 3,029,064 kg / 최소 890,830 kg / 최대 4,447,700 kg / 표준편차 747,053 kg

---

## 현재 상태 (2026-05-14 기준)

- [x] 데이터 파일 확보
- [x] README.md 초안 작성
- [x] REVIEW.md 작성 (프로젝트 리뷰 및 개선사항)
- [ ] 연구 질문(Research Question) 미확정
- [ ] 폴더 구조 미생성 (`src/`, `configs/`, `experiments/`, `results/`)
- [ ] `notebooks/00_overview.ipynb` 미작성 (파일은 있으나 내용 없음)
- [ ] 코드 없음

---

## 주요 논의 사항

### README 내용은 신뢰하지 말 것
README에 기술된 실험 계획(`pca_config.yaml`, `lstm_ae_config.yaml`, `exp01_pca`, `exp02_fault_detection`)은 실제 구현된 것이 아니라 계획 단계의 폴더/파일명입니다. 데이터 기반으로 연구 주제를 새로 도출 중입니다.

### 데이터 기반 연구 주제 도출 중
사용자가 README를 무시하고 데이터 자체를 기반으로 적합한 논문 주제를 탐색 중입니다. Python 실행 환경이 필요합니다 (다음 세션에서 확인 필요).

---

## 다음 세션 우선 과제

1. Python 실행 환경 확인 및 데이터 EDA 수행
2. 연구 주제 확정
3. `notebooks/00_overview.ipynb` 작성 시작
