# Work C — Simulated analysis

대화에서 마지막으로 정리한 4페이지 A–C 보고서용 간소화 버전을 복원했습니다.
`Simulated_analysis.ipynb`에는 한국어 설명과 실행된 표·그림이 있습니다.
`Simulated_analysis.py`는 같은 내용의 제출용 스크립트입니다.

## 분석 범위

- WorkB와 동일한 seed=42 데이터 두 개
- Boxplot과 Q–Q plot으로 가정 점검
- 양측 Welch t-test, 평균 차이, p값, 95% 신뢰구간
- H0/H1 각각 5,000회 반복, 오류율·검정력과 효과 추정치 분포
- 표본 크기와 개인차가 결과에 미치는 영향 해석

## 실행

WorkC 폴더에서:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe build_notebook.py
```

노트북에서는 `.venv` Python을 커널로 선택하고 WorkC를 작업 디렉터리로 사용합니다.
스크립트만 실행하려면 `.\.venv\Scripts\python.exe Simulated_analysis.py`를 사용합니다.
빠른 연습은 `N_REPS`를 줄이되 보고서 수치 재현에는 기본값을 사용합니다.
`build_notebook.py`는 노트북을 덮어쓰므로 수정은 `.py`에 반영하세요.

`outputs/`에 CSV 결과와 보고서 그림 1·2·3에 해당하는
`report_datasets.png`, `report_qq.png`, `report_effects.png`가 저장됩니다.
복원에 사용한 패키지 버전은 이전 실행에 맞춰 `requirements.txt`에 고정했습니다.

## 보고서 보조 파일

`build_abc_report.py`도 복원했습니다. `reportlab`, `pypdf`가 있는 Python으로 실행하면
이전과 같은 `../output/pdf/ADAMS_Report_ABC.pdf`를 생성합니다.
첨부했던 Part A 원본은 코드에 지정된 Downloads 경로에 있어야 합니다.
`report_figures.py`는 현재 분석 그림을 보고서 작업용 임시 폴더에 복사합니다.
두 파일은 제출용 분석 스크립트와 별개입니다.
