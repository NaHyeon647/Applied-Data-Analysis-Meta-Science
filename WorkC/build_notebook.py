"""Convert the commented submission script into an executed Jupyter notebook."""
from pathlib import Path
import os
import re
import sys
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpec

root = Path(__file__).resolve().parent
(root / '.jupyter' / 'ipython').mkdir(parents=True, exist_ok=True)
(root / '.jupyter' / 'runtime').mkdir(parents=True, exist_ok=True)
os.environ['MPLBACKEND'] = 'module://matplotlib_inline.backend_inline'
os.environ['JUPYTER_PLATFORM_DIRS'] = '1'
os.environ['IPYTHONDIR'] = str(root / '.jupyter' / 'ipython')
os.environ['JUPYTER_RUNTIME_DIR'] = str(root / '.jupyter' / 'runtime')
source = (root / 'Simulated_analysis.py').read_text(encoding='utf-8-sig')
parts = re.split(r'^# %%(.*)\n', source, flags=re.MULTILINE)
cells = []
for marker, body in zip(parts[1::2], parts[2::2]):
    body = body.strip()
    if '[markdown]' in marker:
        body = '\n'.join(line[2:] if line.startswith('# ') else '' if line == '#' else line
                         for line in body.splitlines())
        cells.append(nbformat.v4.new_markdown_cell(body))
    else:
        cells.append(nbformat.v4.new_code_cell(body))
notebook = nbformat.v4.new_notebook(cells=cells, metadata={
    'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
    'language_info': {'name': 'python', 'version': sys.version.split()[0]},
})
target = root / 'Simulated_analysis.ipynb'
nbformat.write(notebook, target)
manager = KernelManager(kernel_name='python3')
manager._kernel_spec = KernelSpec(argv=[sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
                                 display_name='Python 3', language='python')
client = NotebookClient(notebook, km=manager, timeout=300, resources={'metadata': {'path': str(root)}})
try:
    client.execute()
finally:
    nbformat.write(notebook, target)
    if manager.has_kernel:
        manager.shutdown_kernel(now=True)
nbformat.validate(notebook)
assert not [o for c in notebook.cells if c.cell_type == 'code'
            for o in c.outputs if o.output_type == 'error']
print(f'Executed and validated {len(cells)} cells: {target}')
