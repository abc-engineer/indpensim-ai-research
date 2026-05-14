# CLAUDE.md — IndPenSim AI Research

이 파일은 Claude Code가 다음 세션에서 프로젝트 컨텍스트를 빠르게 파악하기 위한 문서입니다.

---

## 프로젝트 개요

- **목적**: 석사 논문 작성을 위한 연구 저장소
- **주제**: IndPenSim(Industrial Penicillin Simulation) 데이터셋을 활용한 바이오제약 배치 공정 AI 연구
- **확정 연구 주제**: 딥러닝 기반 이상 감지 (MSPC vs LSTM Autoencoder)
- **언어**: Python

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

---

## 현재 상태 (2026-05-14 기준)

- [x] 데이터 파일 확보
- [x] README.md 초안 작성
- [x] REVIEW.md 작성
- [x] `notebooks/00_overview.ipynb` EDA 코드 작성 및 실행 완료
- [x] 연구 주제 확정: **주제 B — 딥러닝 기반 이상 감지**
- [x] 폴더 구조 생성 (`src/`, `configs/`, `experiments/`, `results/`)
- [x] `src/preprocessing.py` 작성 완료
- [x] `src/models.py` 작성 완료 (LSTM Autoencoder)
- [x] `src/trainer.py` 작성 완료
- [x] `configs/fault_detection.yaml` 작성 완료
- [x] `notebooks/01_fault_detection.ipynb` (Colab용) 작성 완료
- [x] `notebooks/01_fault_detection_local.ipynb` (로컬용) 작성 완료
- [ ] 실험 실행 및 결과 확인
- [ ] 하이퍼파라미터 튜닝
- [ ] Transformer-AE 비교 모델 추가

---

## 프로젝트 파일 구조

```
indpensim-ai-research/
├── configs/
│   └── fault_detection.yaml      # 하이퍼파라미터 설정
├── data/
│   └── raw/                      # CSV 데이터 (gitignore)
├── notebooks/
│   ├── 00_overview.ipynb         # EDA 노트북
│   ├── 01_fault_detection.ipynb  # 실험 노트북 (Colab용)
│   └── 01_fault_detection_local.ipynb  # 실험 노트북 (로컬용)
├── src/
│   ├── preprocessing.py          # 데이터 로드, 정규화, 윈도우 생성
│   ├── models.py                 # LSTM Autoencoder
│   └── trainer.py                # 학습, 평가, 이상 점수
├── experiments/
│   └── exp01_fault_detection/
├── results/
│   ├── figures/                  # 그래프 저장
│   ├── models/                   # 모델 가중치 (.pth)
│   └── logs/                     # 평가 결과 CSV
├── CLAUDE.md
├── REVIEW.md
└── README.md
```

---

## 실험 설계 (Exp01)

### 방법론
| 구분 | 방법 | 비고 |
|------|------|------|
| 기준선 | MSPC (PCA 기반 SPE 통계량) | 전통적 통계 공정 관리 |
| 제안 모델 | LSTM Autoencoder | 재구성 오차 = 이상 점수 |
| 학습 전략 | Normal 배치만으로 학습 | 비지도 이상 감지 |
| 평가 지표 | AUROC, AUPRC, ROC Curve | |

### 사용 변수
- 온라인 공정 변수 24개 (`src/preprocessing.py`의 `ONLINE_VARS`)
- 오프라인 측정 변수(PAA_offline, NH3_offline, P_offline 등) 제외

### 하이퍼파라미터 (`configs/fault_detection.yaml`)
- window_size: 50, stride_train: 10, stride_eval: 1
- hidden_dim: 64, latent_dim: 32, n_layers: 1
- epochs: 50, batch_size: 64, lr: 0.001

---

## 주요 버그 이력 및 해결

| 문제 | 원인 | 해결 |
|------|------|------|
| `KeyError: 'Batch_ref'` | README 기반 잘못된 컬럼명 | 실제 컬럼명으로 수정, 상수 정의 |
| `KeyError: 2` | 메인 CSV 배치 ID가 float, 통계 CSV는 int | `astype(float).astype(int)` + 교집합 처리 |
| `ConnectionAbortedError` | Google Drive에서 2.4GB 직접 읽기 | Drive → 로컬 복사 후 읽기 / 로컬 전용 노트북 분리 |

---

## 주요 주의 사항

- **README 내용 무시**: README의 실험 계획은 미구현 상태였음. 현재는 `src/`, `configs/` 기준으로 관리
- **Colab matplotlib 한글 미지원**: 그래프 제목·축 레이블은 영문, 마크다운·print문은 한글 사용
- **배치 ID 타입**: 메인 CSV는 float, 통계 CSV는 int → 항상 `int`로 통일해서 사용
- **대용량 파일**: Google Drive에서 직접 읽지 말고 로컬로 복사 후 사용

---

## 다음 세션 우선 과제

1. 실험 실행 결과 확인 (AUROC, AUPRC)
2. 결과에 따라 하이퍼파라미터 튜닝
3. Transformer-AE 비교 모델 구현 (`src/models.py` 추가)
