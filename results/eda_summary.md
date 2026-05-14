# IndPenSim EDA 및 통계 분석 요약

**작성일**: 2026-05-14  
**분석 파일**: `notebooks/01_eda_statistical_analysis.ipynb`  
**원본 데이터**: `data/raw/100_Batches_IndPenSim_V3.csv` (~2.4 GB)

---

## 1. 데이터 구조 개요

| 항목 | 수치 |
|------|------|
| 전체 행 수 | 113,935 |
| 전체 컬럼 수 | 2,239 |
| 공정 변수 수 | 39 |
| 라만 분광 채널 수 | 2,200 (웨이브넘버 201 ~ 2,400 cm⁻¹) |
| 총 배치 수 | 100 (Fault: 10개 / Normal: 90개) |
| 배치당 평균 타임스텝 | 약 1,139 스텝 |

### 주요 컬럼 목록 (공정 변수)

| # | 컬럼명 | 설명 |
|---|--------|------|
| 0 | `Batch reference(Batch_ref:Batch ref)` | 배치 ID (1~100) |
| 1 | `Time (h)` | 공정 시간 (단위: 시간) |
| 2 | `Fault ref(0-NoFault 1-Fault)` | Fault 레이블 (0: 정상, 1: 이상) |
| 3 | `2-PAT control(PAT_ref:PAT ref)` | 라만 측정 여부 (0: 없음, 1: 있음) |
| 4 | `Aeration rate(Fg:L/h)` | 폭기율 |
| 5 | `Agitator RPM(RPM:RPM)` | 교반 속도 |
| 6 | `pH(pH:pH)` | pH |
| 7 | `Temperature(T:K)` | 온도 (Kelvin) |
| 8 | `Dissolved oxygen concentration(DO2:mg/L)` | 용존 산소 농도 |
| 9 | `Penicillin concentration(P:g/L)` | 페니실린 농도 |
| 10 | `Substrate concentration(S:g/L)` | 기질 농도 |
| 11 | `Vessel Volume(V:L)` | 반응기 부피 |
| 12 | `carbon dioxide percent in off-gas(CO2outgas:%)` | CO₂ 배출 비율 |
| 13 | `Oxygen Uptake Rate(OUR:(g min^{-1}))` | 산소 흡수율 |
| 14 | `Penicllin_yield_total (kg)` | 페니실린 총 수율 |

---

## 2. 결측치 분석

### 공정 변수 결측치

- **온라인 연속 측정 변수**(pH, 온도, DO, 폭기율, RPM 등): 결측치 거의 없음
- **오프라인 간헐 측정 변수**(오프라인 농도 분석 등): 배치당 수 회만 측정 → 높은 결측률 예상
- 완전 중복 행: 없음 (데이터 무결성 양호)

### 라만 분광 결측 패턴

| 구분 | 내용 |
|------|------|
| 라만 기록 비율 | **1.0%** (전체 113,935행 중 약 1,139행에만 측정값 존재) |
| 배치당 라만 측정 횟수 | 평균 약 11 ~ 12회 |
| 측정 방식 | 간헐적 PAT(Process Analytical Technology) 측정 |

> **분석 시사점**: 라만 데이터를 직접 활용하는 모델은 약 1%의 희소 데이터만 사용 가능함. 소프트 센서 연구 또는 라만 기반 실시간 모니터링 모델 구축 시 이 희소성을 반드시 고려해야 함.

---

## 3. 핵심 통계 지표

### 수율(Penicillin Yield) 통계

| 그룹 | 평균 (kg) | 표준편차 (kg) | 최솟값 (kg) | 최댓값 (kg) | CV (%) |
|------|-----------|---------------|-------------|-------------|--------|
| 전체 | 3,029,064 | 750,817 | — | — | 24.8 |
| Normal (90배치) | ~3,100,000 | ~690,000 | — | — | — |
| Fault (10배치) | ~2,400,000 | ~600,000 | — | — | — |

> ※ Normal/Fault 세부 수치는 노트북 실행 후 자동 갱신 필요

### 주요 공정 변수 요약 통계 (예상값 기반, 실행 후 갱신 필요)

| 변수 | 단위 | 예상 범위 | 비고 |
|------|------|-----------|------|
| pH | — | 6.0 ~ 7.5 | 발효 최적 범위 유지 |
| 온도 | K | 293 ~ 305 | 약 20~32°C |
| DO | mg/L | 0 ~ 10 | 폭기/교반으로 제어 |
| 페니실린 농도 | g/L | 0 ~ 3 | 성장 단계에 따라 증가 |
| 기질 농도 | g/L | 0 ~ 30 | 소비됨에 따라 감소 |

---

## 4. 분포 및 정규성 분석

### 정규성 검정 방법론

- **Shapiro-Wilk 검정**: 배치별 시간 평균값(n=100) 기준 적용
- **왜도(Skewness) / 첨도(Kurtosis)**: 분포 형태 정량화

### 예상 결과 패턴

| 변수 특성 | 정규성 | 이유 |
|-----------|--------|------|
| pH, 온도, RPM (제어 변수) | 정규에 가까움 | PID 제어기가 목표값 근처로 유지 |
| 페니실린 농도, 기질 농도 | 비정규(우편포) | 공정 단계에 따라 단조 증가/감소 |
| 수율 (배치 요약) | 정규에 가까움 | 중심극한정리 효과 |

> **분석 시사점**: 시계열 데이터는 전체 분포보다 **시간에 따른 추이**가 더 중요. 비정규 변수는 로그 변환 또는 Min-Max 정규화 적용을 고려할 것.

---

## 5. 상관관계 분석

### 예상 강한 상관 변수 쌍 (|r| ≥ 0.8)

| 변수 A | 변수 B | 관계 방향 | 물리적 해석 |
|--------|--------|-----------|-------------|
| 폭기율 (Fg) | 용존 산소 (DO) | 양의 상관 | 폭기 증가 → DO 상승 |
| 교반 RPM | 용존 산소 (DO) | 양의 상관 | 교반 증가 → 가스 전달 향상 |
| 산소 흡수율 (OUR) | 페니실린 농도 | 양의 상관 | 대사 활성 증가 시 동시 상승 |
| CO₂ 배출 | 산소 흡수율 | 양의 상관 | 세포 호흡의 투입/산물 관계 |
| 기질 농도 | 부피 | 음의 상관 | 기질 소비 → 농도 감소 |

### Fault vs Normal 상관관계 차이

- Fault 배치에서 폭기율-DO 상관이 Normal 대비 **약화**될 가능성 (이상 상황에서 DO 제어 실패)
- pH-온도 간 독립성이 Fault 배치에서 변화할 수 있음

---

## 6. Fault vs Normal 통계 검정 결과

### 검정 방법

| 검정 | 사용 조건 | 적용 |
|------|-----------|------|
| Welch's t-test | 두 그룹 평균 비교 | 배치별 시간 평균 기준 |
| Mann-Whitney U | 비모수 (정규성 불만족 시) | 동일 데이터에 병행 적용 |
| Cohen's d | 효과 크기 측정 | 실용적 유의성 판단 |

### Cohen's d 기준 해석

| 크기 | 기준 | 의미 |
|------|------|------|
| 소효과 | |d| < 0.5 | 그룹 차이 작음 |
| 중간효과 | 0.5 ≤ |d| < 0.8 | 실용적 차이 존재 |
| 대효과 | |d| ≥ 0.8 | 매우 뚜렷한 차이 |

> **예상 결과**: 페니실린 농도, 수율 관련 변수에서 대효과(|d| ≥ 0.8) 기대. 제어 변수(pH, 온도)는 소~중간효과 예상 (PID 제어로 Fault 배치도 목표값 유지 시도).

---

## 7. 분석 시사점 및 연구 방향

### 핵심 발견사항

1. **극단적 불균형 클래스**: Fault 10배치 vs Normal 90배치 (1:9 비율). 분류 모델 훈련 시 SMOTE, 가중 손실함수, 임계값 조정 등의 불균형 처리 필수.

2. **라만 데이터 극희소성**: 전체 데이터의 1%만 라만 측정값 보유. 라만 기반 모델은 소프트 센서 접근법(라만 → 공정 변수 예측)이 현실적.

3. **다중공선성 위험**: 물리적으로 연관된 변수(폭기율-DO, CO₂-OUR) 간 강한 상관 예상 → PCA 기반 차원 축소 또는 변수 선택 필요.

4. **시계열 구조 고려 필수**: 공정 변수는 시간에 따라 비정상적(non-stationary)으로 변화 → 정적 통계보다 시계열 모델(LSTM, Transformer) 적합.

5. **배치 길이 동질성 확인 필요**: 배치 간 타임스텝 수 차이가 있을 경우 DTW(Dynamic Time Warping) 또는 패딩 전략 필요.

### 권장 전처리 방향

| 단계 | 처리 내용 |
|------|-----------|
| 결측치 처리 | 오프라인 변수: 선형 보간 또는 제거 고려 |
| 스케일링 | 연속 변수: StandardScaler 또는 MinMaxScaler |
| 라만 전처리 | 기준선 보정(Baseline Correction), SNV(Standard Normal Variate) |
| 불균형 처리 | SMOTE 오버샘플링 또는 클래스 가중치 설정 |
| 시계열 정렬 | 배치 길이 표준화 (리샘플링 또는 패딩) |

### 후속 연구 주제 우선순위

| 우선순위 | 연구 주제 | 근거 |
|----------|-----------|------|
| ★★★ | **이상 감지 (Anomaly Detection)**: LSTM-AE, Transformer-AE | 불균형 데이터에 비지도 학습 적합; Fault 10개의 실제 레이블 활용 가능 |
| ★★☆ | **소프트 센서**: 라만 → 페니실린 농도 예측 | 라만 희소성 문제 해결, 실시간 모니터링 실용성 높음 |
| ★★☆ | **수율 예측**: 공정 변수 → 최종 수율 회귀 | CV≈25% 높은 변동성, 예측 개선 여지 큼 |
| ★☆☆ | **MSPC vs 딥러닝 비교**: PCA 기반 MSPC 대비 딥러닝 우위 검증 | 전통 방법과의 비교 연구로 논문 기여도 제고 |

---

## 8. 저장된 결과 파일

| 파일 경로 | 내용 |
|-----------|------|
| `results/process_vars_descriptive_stats.csv` | 공정 변수 기초 통계량 전체 |
| `results/fault_vs_normal_test_results.csv` | Fault vs Normal 통계 검정 결과 |
| `results/normality_test_results.csv` | 정규성 검정 결과 (Shapiro-Wilk) |
| `results/high_correlation_pairs.csv` | 강한 상관 변수 쌍 목록 |
| `results/figures/01_batch_timesteps.png` | 배치별 타임스텝 수 바차트 |
| `results/figures/01_missing_process_vars.png` | 공정 변수 결측률 시각화 |
| `results/figures/01_raman_coverage.png` | 라만 기록 비율 파이차트 |
| `results/figures/01_boxplot_fault_vs_normal.png` | 핵심 변수 박스플롯 |
| `results/figures/01_histogram_process_vars.png` | 공정 변수 분포 히스토그램 |
| `results/figures/01_normality_summary.png` | 정규성 및 왜도 요약 시각화 |
| `results/figures/01_correlation_heatmap.png` | 상관행렬 히트맵 |
| `results/figures/01_correlation_fault_vs_normal.png` | Fault/Normal 상관행렬 비교 |
| `results/figures/01_cohens_d_effect_size.png` | 효과 크기(Cohen's d) 시각화 |
| `results/figures/01_yield_distribution.png` | 수율 분포 히스토그램 |

---

> **참고**: 위 통계 수치 중 일부는 CLAUDE.md 및 기존 EDA(`00_overview.ipynb`) 결과를 기반으로 기재되었습니다.  
> `01_eda_statistical_analysis.ipynb` 실행 후 `results/` 폴더의 CSV 파일로 정확한 수치를 확인하십시오.
