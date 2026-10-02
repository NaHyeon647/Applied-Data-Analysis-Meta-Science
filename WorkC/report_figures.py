"""Copy the analysis figures for report assembly without running another analysis."""
from pathlib import Path
from shutil import copy2

root = Path(__file__).resolve().parents[1]
target = root / 'tmp' / 'pdfs'
target.mkdir(parents=True, exist_ok=True)
for name in ['report_datasets.png', 'report_qq.png', 'report_effects.png']:
    source = root / 'WorkC' / 'outputs' / name
    if not source.exists():
        raise FileNotFoundError('Run build_notebook.py first to generate the figures.')
    copy2(source, target / name)
print('Copied the three current analysis figures for the report.')
