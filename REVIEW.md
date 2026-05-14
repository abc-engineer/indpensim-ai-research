# 프로젝트 리뷰: IndPenSim AI Research

> 작성일: 2026-05-14

---

## 현재 상태 요약

| 항목 | 내용 |
|------|------|
| **주제** | IndPenSim 데이터 기반 바이오제약 배치 공정 AI 연구 |
| **데이터** | 100배치, ~113,936행, ~2.4 GB (공정변수 30개 + 라만 분광 2,400 채널) |
| **목표 실험** | PCA 기반 분석 + Fault Detection (LSTM-AE 계획) |
| **실제 구현** | README + 데이터 파일만 존재, 코드 없음 |

---

## 주요 문제점

### 1. 구조만 있고 실체가 없음

README에 `configs/`, `src/`, `experiments/`, `results/` 폴더가 정의되어 있으나 실제로는 존재하지 않습니다.  
`notebooks/00_overview.ipynb`도 완전히 비어있습니다.

### 2. 연구 질문(Research Question)이 불명확

README를 읽어도 **"무엇을 증명하려는 연구인가"**가 보이지 않습니다.  
Fault detection인지, 공정 최적화인지, Raman 스펙트럼 활용인지 범위가 열려있습니다.

### 3. `data/README.md`가 불완전

> "Download instructions are provided here."

라고 적혀있지만 실제 다운로드 방법이 없습니다. 재현 가능성(reproducibility) 측면에서 중요합니다.

### 4. 저자 정보 누락

```
Name:  
Affiliation:  
Contact:  
```

공개 저장소라면 최소한 소속 기관은 기재해야 합니다.

### 5. `.gitignore` 범위가 좁음

현재 `data/raw/*`만 무시하는데, `data/processed/`, `results/`, `*.pth` 모델 파일 등도 고려해야 합니다.

---

## 데이터 관련 주의사항

- 메인 CSV에 **라만 분광 2,400 컬럼**이 포함되어 있어 고차원 데이터입니다. PCA 전처리가 필수적입니다.
- 통계 파일에서 Fault 레이블이 있어 지도학습도 가능하지만, 계획상 LSTM-AE는 비지도 이상 감지로 보입니다. 두 접근 방식의 비교 전략을 명확히 해야 합니다.
- 100배치 중 fault 비율이 얼마인지 아직 확인 안 된 상태입니다.

---

## 권장 다음 단계 (우선순위 순)

1. **`00_overview.ipynb` 작성** — EDA (데이터 형태, 결측치, fault 비율, 변수 분포)
2. **연구 질문 확정** — 논문의 contribution을 한 문장으로 정리
3. **폴더 구조 실제 생성** — `src/preprocessing.py`부터 뼈대 구현
4. **`data/README.md` 보완** — 다운로드 절차 및 전처리 재현 방법 기술
