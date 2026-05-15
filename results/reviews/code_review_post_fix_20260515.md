# 코드 리뷰 결과 — 수정 후 검증 (2026-05-15)

## 검토 대상
- `notebooks/00_overview.ipynb`
- `notebooks/01_eda_statistical_analysis.ipynb`

---

## 1순위: 잔존 버그 및 새로운 오류

### [CRITICAL] 00_overview.ipynb — EDA 요약 셀에서 PAT_COL 오용 잔존

**파일**: `notebooks/00_overview.ipynb`, cell-24

```python
print(f'  라만 기록 비율     : {(df[PAT_COL]==1).mean()*100:.1f}%')
```

`PAT_COL`('2-PAT control')은 배치 번호(1~100)를 담고 있으므로 `== 1`은 배치 1번 행만 선택 → 1.0%라는 잘못된 값 출력. `01_eda`의 code-summary-print는 `df[raman_cols[0]].astype(float) != 0`으로 올바르게 수정되어 있으나 `00_overview`에는 미적용.

---

### [HIGH] 00_overview.ipynb — PAT_COL에 잘못된 dtype 지정 유지

**파일**: `notebooks/00_overview.ipynb`, cell-04

```python
_dtype_map[PAT_COL] = 'Int8'
```

PAT_COL이 배치 번호(1~100)임이 확인됐음에도 Int8 지정 유지. `01_eda`에서는 제거 및 주석 처리됐으나 `00_overview`에 미반영.

---

### [HIGH] 01_eda_statistical_analysis.ipynb — 섹션 4 마크다운에 구버전 설명 잔존

**파일**: `notebooks/01_eda_statistical_analysis.ipynb`, md-sec4

```markdown
- 라만 데이터의 결측 패턴 (PAT_ref 기반)
```

코드에서 PAT_ref 기반 방식 폐기 후 라만 채널 값 기반으로 수정했으나 마크다운 미수정.

---

### [HIGH] 00_overview.ipynb — process_cols에 batch_number 컬럼 포함

**파일**: `notebooks/00_overview.ipynb`, cell-06

`process_cols = [c for c in df.columns if c not in raman_cols]`로 생성 시 `batch_number`가 포함되어 공정 변수 수가 40개로 집계됨 (정확값: 39). 결측치 분석, 상관 분석 대상에도 포함됨.

올바른 수정 방향:
```python
process_cols = [c for c in df.columns if c not in raman_cols and c != BATCH_NUM_COL]
```

---

## 2순위: 성능 및 로직 문제

### [MEDIUM] PerformanceWarning — 컬럼 삽입으로 인한 DataFrame 파편화

**파일**: `notebooks/00_overview.ipynb`, cell-04 출력

2,200개 라만 컬럼 로드 후 `batch_number` 컬럼 삽입 시 PerformanceWarning 발생. `01_eda`는 `warnings.filterwarnings('ignore')`로 억제되지만 실제 성능 저하는 존재.

개선 방향: `pd.concat` 사용 또는 `df.copy()`를 통한 파편화 해소.

### [MEDIUM] Statistics CSV FAULT_COL 컬럼명 불일치 잠재 위험

`FAULT_COL`은 메인 V3 CSV용 상수인데 Statistics CSV에도 동일 이름을 사용 중. 분리 권장:
```python
FAULT_COL_STATS = 'Fault ref(0-NoFault 1-Fault)'
```

### [MEDIUM] Cohen's d 계산 공식 불정확

**파일**: `notebooks/01_eda_statistical_analysis.ipynb`, code-statistical-test

Fault(10개) vs Normal(90개)처럼 표본 크기 차이가 클 때 단순 평균 pooled SD는 과소추정. 표준 가중 공식 권장:
```python
pooled_std = np.sqrt(((n1-1)*s1**2 + (n2-1)*s2**2) / (n1+n2-2))
```

---

## 3순위: 가독성 및 스타일

### [STYLE] 01_eda — exclude_cols 변수 재정의로 상위 스코프 덮어쓰기

code-basic-stats에서 정의된 `exclude_cols`를 code-group-stats에서 다른 내용으로 재정의. `exclude_cols_group`처럼 별도 이름 사용 권장.

### [STYLE] 00_overview — key_vars 변수 이름 중복 사용

셀-11: 6개 변수, 셀-22: 11개 변수로 재정의. `ts_vars`, `corr_vars` 등으로 분리 권장.

---

## 이전 버그 수정 검증 결과

| 이전 버그 | 수정 여부 | 비고 |
|---|---|---|
| BATCH_COL 이진 플래그 오용 | ✅ 완료 | Time 리셋 기반 batch_number 생성 |
| 배치 수 오산출 | ✅ 완료 | nunique() 사용, 100 출력 확인 |
| 라만 측정 횟수 오산출 | 🟡 부분 완료 | 01 완료, 00 요약 셀 미수정 |
| 부분 중복 탐지 오류 | ✅ 완료 | BATCH_NUM_COL 사용, 0건 |
| Agitator RPM 제로분산 NaN 처리 | ✅ 완료 | 'N/A (zero variance)' |
| t-검정 NaN 전파 | ✅ 완료 | np.isnan(p_ttest) 체크 |
| FAULT_COL Int8 dtype 누락 | ✅ 완료 | 조건부 적용 |
| results/figures 디렉터리 미생성 | ✅ 완료 | mkdir(exist_ok=True) |
| savefig 누락 | ✅ 완료 | 모든 플롯에 추가 |
| PAT_COL 라만 지표 오용 | 🟡 부분 완료 | 01 완료, 00 요약 셀 미수정 |

---

## 조치 권고 우선순위

1. **즉시 수정**: `00_overview.ipynb` 셀-24의 `(df[PAT_COL]==1).mean()*100` → `df[raman_cols[0]].astype(float) != 0`
2. **즉시 수정**: `00_overview.ipynb` cell-04의 `_dtype_map[PAT_COL] = 'Int8'` 제거
3. **수정 권고**: `00_overview.ipynb` cell-06에서 `process_cols` 생성 시 `batch_number` 제외
4. **수정 권고**: `01_eda` 섹션 4 마크다운에서 "(PAT_ref 기반)" 제거
5. **개선 권고**: Cohen's d pooled SD 계산식 표본 크기 가중 방식으로 교체
6. **개선 권고**: `exclude_cols`, `key_vars` 변수 이름 충돌 해소
