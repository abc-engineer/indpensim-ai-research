# 코드 리뷰 결과 — 2026-05-15

## 검토 범위

- `notebooks/00_overview.ipynb`
- `notebooks/01_eda_statistical_analysis.ipynb`
- `src/` 폴더: Python 파일 없음 (검토 대상 없음)

---

## 1순위: 오류 가능성 (버그, 잠재적 크래시)

### [CRITICAL-01] `00_overview.ipynb` — `BATCH_COL` 이진 플래그를 배치 ID로 잘못 사용

`BATCH_COL = 'Batch reference(Batch_ref:Batch ref)'` 컬럼은 **0 또는 1만 가지는 이진 플래그**입니다. 그러나 `00_overview.ipynb`의 cell-07에서 이 컬럼을 배치 ID처럼 사용합니다.

```python
# cell-07: 잘못된 코드
batch_lengths = df[BATCH_COL].value_counts().sort_index()
print(f'배치 수 : {batch_lengths.shape[0]}')  # → 2 (0, 1만 출력됨)
```

이로 인해 이어지는 cell-11, cell-15, cell-21 등에서 `df[BATCH_COL].isin(fault_ids)` 필터링이 모두 빈 DataFrame을 반환하거나, 전혀 의도치 않은 데이터를 추출하게 됩니다. `01_eda_statistical_analysis.ipynb`에서는 `Time (h)` 리셋 기반으로 `batch_number` 컬럼을 올바르게 생성하여 수정되어 있으나, **`00_overview.ipynb`는 이 수정이 적용되지 않은 채로 남아 있습니다.** 해당 노트북의 모든 배치 단위 분석 결과가 무의미합니다.

---

### [CRITICAL-02] `01_eda_statistical_analysis.ipynb` `code-summary-print` 셀 — `BATCH_COL`로 배치 수 오산출

```python
# 잘못된 코드
print(f'  배치 수  : {df[BATCH_COL].nunique()} (Fault: 10, Normal: 90)')
# 실제 출력: 배치 수 : 2 (Fault: 10, Normal: 90)
```

`df[BATCH_NUM_COL].nunique()`로 교체해야 합니다.

---

### [CRITICAL-03] `01_eda_statistical_analysis.ipynb` `code-summary-print` 셀 — 라만 측정 횟수 오산출

```
# 실제 출력: 배치당 라만 측정 횟수 : 평균 1130.0회
```

실제 기댓값은 약 11~12회입니다. `groupby` 대상 컬럼이 잘못되었거나 셀 실행 순서 문제로 `BATCH_NUM_COL`이 생성되기 전에 계산된 것으로 추정됩니다.

---

### [HIGH-01] `01_eda_statistical_analysis.ipynb` `code-duplicates` 셀 — `BATCH_COL` 이진 플래그로 부분 중복 탐지

```python
# 잘못된 코드
dup_partial = df.duplicated(subset=[BATCH_COL, TIME_COL]).sum()
# 출력: (배치 ID + Time) 중복 행 수: 111195
```

`BATCH_COL`이 0/1 이진 플래그이므로 실제 중복이 아닌 허위 경고 111,195건이 발생합니다. `BATCH_NUM_COL`을 사용해야 합니다.

---

### [HIGH-02] `01_eda_statistical_analysis.ipynb` `code-normality-test` 셀 — `Agitator RPM` Shapiro-Wilk 결과 NaN

`Agitator RPM`은 모든 값이 100.0으로 분산이 0입니다. `stats.skew()`, `stats.kurtosis()`가 NaN을 반환하며 이후 `abs(s) > 1` 조건에서 `False`로 평가되어 시각화가 오염됩니다. 분산이 0인 변수는 사전에 필터링하거나 NaN을 명시적으로 처리해야 합니다.

---

### [HIGH-03] `01_eda_statistical_analysis.ipynb` `code-statistical-test` 셀 — 분산 0 변수에서 t-검정 NaN 전파

```python
t_stat, p_ttest = stats.ttest_ind(batch_mean_fault, batch_mean_nofault, equal_var=False)
```

`Agitator RPM`에서 `t_stat=NaN`, `p_ttest=NaN`이 반환되어 `significance` 컬럼에 'not significant'로 잘못 분류됩니다. 분산 0인 경우 'N/A (zero variance)' 처리가 필요합니다.

---

### [MEDIUM-01] `00_overview.ipynb` `cell-19` — `BATCH_COL == 1`로 오프라인 변수 조회

```python
batch1 = df[df[BATCH_COL] == 1]
```

"1번 배치"가 아닌 "플래그 값이 1인 모든 행"이 선택됩니다.

---

### [MEDIUM-02] `01_eda_statistical_analysis.ipynb` `code-load-strategy-a` 셀 — `FAULT_COL` dtype 지정 누락

```python
dtype_map = {col: 'float32' for col in raman_cols}
dtype_map[PAT_COL] = 'Int8'
# FAULT_COL Int8 지정 누락 — CLAUDE.md "PAT/Fault는 Int8 dtype 지정 필요" 위반
```

---

## 2순위: 성능 문제

### [PERF-01] `00_overview.ipynb` `cell-04` — dtype 최적화 없이 전체 로드

```python
df = pd.read_csv(MAIN_PATH)
```

라만 2,200컬럼이 `float64`로 로드되어 `float32` 대비 약 2배 메모리 사용.

---

### [PERF-02] `00_overview.ipynb` `cell-15` — `.astype(float)` 중복 호출

`df_raman` 생성 시 이미 적용했음에도 매번 `.astype(float)` 재호출.

---

### [PERF-03] `01_eda_statistical_analysis.ipynb` `code-group-stats` 셀 — `is_numeric_dtype` 중복 계산

`code-basic-stats` 셀의 `numeric_process_cols`와 동일한 계산을 `numeric_process_cols_tmp`로 재수행.

---

### [PERF-04] `01_eda_statistical_analysis.ipynb` `code-load-strategy-a` 셀 — 헤더 읽기용 별도 I/O

```python
header_df = pd.read_csv(MAIN_PATH, nrows=0)
```

컬럼 목록을 위해 2.4 GB 파일을 한 번 더 open.

---

## 3순위: 가독성

### [READ-01] `YIELD_COL` 오타 미검증

`'Penicllin_yield_total (kg)'` — "Penicllin"은 오타. 실제 CSV 컬럼명과 일치하는지 `assert`로 검증 없음.

### [READ-02] 변수명 혼재

`numeric_process_cols` / `numeric_process_cols_tmp` / `key_vars`가 셀마다 별도 정의되어 일관성 없음.

### [READ-03] NaN 색상 처리 누락

`abs(NaN) > 1 → False`로 `Agitator RPM`이 파란색으로 잘못 표시됨.

### [READ-04] `00_overview.ipynb` `cell-12` — `groupby(TIME_COL)` 의미 불명확

배치 길이가 다를 수 있어 특정 시간대에는 일부 배치만 집계되는 점이 주석으로 설명되지 않음.

---

## 4순위: 스타일

### [STYLE-01] `00_overview.ipynb` — `savefig()` 없음

모든 시각화 셀에 저장 로직 없음. CLAUDE.md "그래프: results/figures/" 규칙 위반.

### [STYLE-02] `01_eda_statistical_analysis.ipynb` — `results/figures/` 디렉터리 미생성

```python
RESULTS_DIR.mkdir(exist_ok=True)  # results/만 생성, figures/ 미생성
```

첫 실행 시 `savefig` 호출에서 `FileNotFoundError` 발생 가능.

### [STYLE-03] 주석 처리된 대안 코드 잔존

`code-load-strategy-b` 셀에 청크 로드 코드가 전체 주석 처리된 채로 남아 있음.

### [STYLE-04] `BATCH_COL_STATS` 상수 미사용

정의는 있으나 일부 셀에서 리터럴 문자열로 대체됨.

---

## 종합 요약

| 우선순위 | ID | 위치 | 내용 |
|---|---|---|---|
| CRITICAL | CRITICAL-01 | `00_overview.ipynb` 전체 | `BATCH_COL` 이진 플래그 오용 → 모든 배치 단위 분석 무효 |
| CRITICAL | CRITICAL-02 | `01_eda` `code-summary-print` | 배치 수 2로 잘못 출력 |
| CRITICAL | CRITICAL-03 | `01_eda` `code-summary-print` | 라만 측정 횟수 1130회 오산출 (실제 ~11회) |
| HIGH | HIGH-01 | `01_eda` `code-duplicates` | 허위 중복 111,195건 경고 |
| HIGH | HIGH-02 | `01_eda` `code-normality-test` | Agitator RPM NaN 미처리 |
| HIGH | HIGH-03 | `01_eda` `code-statistical-test` | 분산 0 변수 t-검정 NaN 전파 |
| MEDIUM | MEDIUM-01 | `00_overview.ipynb` `cell-19` | BATCH_COL 오용 |
| MEDIUM | MEDIUM-02 | `01_eda` `code-load-strategy-a` | FAULT_COL Int8 dtype 누락 |
| PERF | PERF-01~04 | 두 노트북 전반 | 메모리/연산 최적화 미흡 |
| READ | READ-01~04 | 두 노트북 전반 | 오타 검증 없음, 변수명 혼재 등 |
| STYLE | STYLE-01~04 | 두 노트북 전반 | savefig 누락, 디렉터리 미생성 등 |

**가장 시급한 수정**: CRITICAL-01~03, 그리고 STYLE-02 (`results/figures/` 디렉터리 자동 생성).
