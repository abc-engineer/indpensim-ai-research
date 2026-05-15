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
- `data/raw/100_Batches_IndPenSim_V3.csv` — 메인 시계열 데이터 (~2.4 GB, 113,935행)
- `data/raw/100_Batches_IndPenSim_Statistics.csv` — 배치별 요약 통계 (100행)

> raw 데이터는 `.gitignore`에 의해 git 추적에서 제외됨. 원본 다운로드: http://www.industrialpenicillinsimulation.com/

### 데이터 구조 (V3 CSV)
- **전체 컬럼 수**: 2,239개
- **공정 변수** (39개): 시간, 폭기율, 교반 RPM, pH, 온도, DO, 페니실린 농도, 부피, 기질 농도 등
- **라만 분광 데이터** (2,200채널): 웨이브넘버 201 ~ 2400 cm⁻¹
- **실제 컬럼명** (코드 작성 시 반드시 사용):
  - 배치 ID (이진 플래그 0/1): `Batch reference(Batch_ref:Batch ref)`
  - 통계 CSV 배치 ID: `Batch ref`
  - Fault 레이블 (통계 CSV): `Fault ref(0-NoFault 1-Fault)`
  - PAT 컬럼: `2-PAT control(PAT_ref:PAT ref)` — **배치 번호(1~100) 저장, 라만 기록 지표 아님**

> ⚠️ **`PAT_ref` 컬럼 주의사항 (2026-05-15 확인)**  
> `'2-PAT control(PAT_ref:PAT ref)'` 컬럼은 **라만 기록 여부가 아닌 배치 번호(1~100)**를 저장함.  
> 실제 라만 기록 여부: **라만 채널 값이 0이 아닌 행** (`df[raman_cols[0]].astype(float) != 0`)  
> 각 배치 첫 10 타임스텝(Time ≤ 2.0h)만 워밍업으로 라만 채널 = 0임.

### ⚠️ 배치 식별 주의사항 (2026-05-15 확인)

`'Batch reference(Batch_ref:Batch ref)'` 컬럼은 **배치 번호가 아닌 이진 플래그(값 0 또는 1)**임.
실제 배치(100개)는 `Time (h)` 컬럼이 감소(리셋)하는 지점으로 구분해야 함.

```python
# 올바른 배치 번호 생성 방법
time_diff = df['Time (h)'].diff()
reset_mask = time_diff.fillna(0) < 0   # True = 새 배치 시작
batch_num  = reset_mask.cumsum() + 1   # 배치 번호 1~100
df['batch_number'] = batch_num.astype(int)
```

Statistics CSV의 `Batch ref` (1~100, float)는 위 `batch_number`와 순서 기준으로 매핑.

### EDA 결과 (2026-05-15 확인)

| 항목 | 수치 |
|------|------|
| 총 배치 수 | 100 (Fault 10개 / Normal 90개) |
| 전체 행 수 | 113,935 |
| 공정 변수 수 | 39 |
| 라만 채널 수 | 2,200 (201~2400 cm⁻¹) |
| **라만 기록 비율** | **99.1%** (배치당 첫 10 타임스텝 워밍업만 제외) |
| 수율 평균 | 3,029,064 kg |
| 수율 표준편차 | 750,817 kg (CV ≈ 24.8%) |

---

## 코딩 컨벤션

- **그래프 텍스트** (제목, 축 레이블, 범례): **영어** (논문 제출 기준)
- **print() 출력 및 코드 주석**: 한국어 유지
- **결과물 저장 경로**:
  - 그래프: `results/figures/`
  - 분석 결과 CSV: `results/`
  - 요약 보고서: `results/`
  - 노트북: `notebooks/`
  - 전처리/모델 함수: `src/`
- **메모리 최적화**: 라만 채널은 `float32` dtype 지정 (PAT_ref는 배치 번호라 특별 처리 불필요)

---

## 서브 에이전트 구성 (`.claude/agents/`)

| 파일 | 역할 |
|------|------|
| `data-analyst.md` | 데이터 탐색, 전처리, 통계 분석 |
| `visualizer.md` | 논문용 그래프 생성 (dpi=300, 영문 레이블) |
| `code-reviewer.md` | 코드 리뷰 |

---

## 현재 상태 (2026-05-15 기준)

- [x] 데이터 파일 확보
- [x] README.md 초안 작성
- [x] REVIEW.md 작성
- [x] 폴더 구조 생성 (`src/`, `configs/`, `experiments/`, `results/`)
- [x] `notebooks/00_overview.ipynb` EDA 코드 작성 및 실행 완료
  - 배치 번호 생성, 라만 기록 지표 수정 (99.1%), savefig 추가
  - 2차 리뷰 버그 수정: PAT_COL Int8 제거, process_cols에서 batch_number 제외 (39개), 라만 비율 출력 수정
- [x] `.claude/agents/` 서브 에이전트 구성 (data-analyst, visualizer, code-reviewer)
- [x] `notebooks/01_eda_statistical_analysis.ipynb` 작성 및 실행 완료
  - 배치 식별 버그 수정 (Time 리셋 기반 배치 번호 생성)
  - 그래프 레이블 영문화
  - 10개 PNG 그래프 생성 (`results/figures/`)
  - 4개 CSV 결과 파일 생성 (`results/`)
  - 2차 리뷰 버그 수정: md-sec4 마크다운 수정, exclude_cols_group 변수명 분리, Cohen's d 표본 크기 가중 pooled SD 적용
- [x] 코드 리뷰 2회 수행 및 전체 지적 사항 수정 완료 (`results/reviews/`)
- [ ] 연구 주제 확정

---

## 생성된 결과물

### 그래프 (`results/figures/`)
| 파일 | 내용 |
|------|------|
| `00_batch_timesteps.png` | 배치별 타임스텝 수 분포 (overview) |
| `00_yield_distribution.png` | 수율 분포 Fault vs Normal (overview) |
| `00_process_vars_timeseries.png` | 핵심 공정 변수 시계열 (overview) |
| `00_penicillin_mean_std.png` | 페니실린 농도 전 배치 평균±Std (overview) |
| `00_raman_spectra.png` | 평균 라만 스펙트럼 + Fault vs Normal 비교 (overview) |
| `00_raman_top20_variance.png` | 분산 상위 20 라만 채널 (overview) |
| `00_missing_values.png` | 공정 변수 결측률 (overview) |
| `00_fault_vs_normal_timeseries.png` | Fault vs Normal 시계열 비교 (overview) |
| `00_correlation_heatmap.png` | 상관행렬 (Normal 배치, overview) |
| `01_batch_timesteps.png` | 배치별 타임스텝 수 분포 |
| `01_missing_process_vars.png` | 공정 변수 결측률 |
| `01_raman_coverage.png` | 라만 분광 기록 비율 (파이 차트) |
| `01_boxplot_fault_vs_normal.png` | Fault vs Normal 박스플롯 |
| `01_histogram_process_vars.png` | 공정 변수 분포 히스토그램 |
| `01_normality_summary.png` | 정규성 검정 결과 + 왜도 |
| `01_correlation_heatmap.png` | 피어슨 상관행렬 (Normal 배치) |
| `01_correlation_fault_vs_normal.png` | Fault vs Normal 상관관계 비교 |
| `01_cohens_d_effect_size.png` | Cohen's d 효과 크기 (표본 크기 가중 pooled SD) |
| `01_yield_distribution.png` | 수율 분포 비교 |

### CSV (`results/`)
| 파일 | 내용 |
|------|------|
| `process_vars_descriptive_stats.csv` | 공정 변수 기초 통계량 |
| `fault_vs_normal_test_results.csv` | Fault vs Normal 통계 검정 결과 |
| `normality_test_results.csv` | 정규성 검정 결과 |
| `high_correlation_pairs.csv` | 강한 상관 변수 쌍 (\|r\|≥0.8) |

### 코드 리뷰 (`results/reviews/`)
| 파일 | 내용 |
|------|------|
| `code_review_20260515.md` | 1차 코드 리뷰 결과 |
| `code_review_post_fix_20260515.md` | 2차 코드 리뷰 결과 (수정 후 검증) |
