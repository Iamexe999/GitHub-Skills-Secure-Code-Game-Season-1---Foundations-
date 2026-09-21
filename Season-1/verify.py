"""Run in a temporary copy so the exercise database stays reproducible."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def run(args, cwd):
    print('$ ' + ' '.join(map(str, args)), flush=True)
    result = subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    print(result.stdout, end='', flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)
    return result.stdout


with tempfile.TemporaryDirectory(prefix='secure-code-game-') as temp:
    root = Path(temp) / 'Season-1'
    shutil.copytree(Path(__file__).resolve().parent, root,
                    ignore=shutil.ignore_patterns('__pycache__', '*.db'))
    for level in range(1, 6):
        folder = root / f'Level-{level}'
        print(f'\n=== LEVEL {level} ===', flush=True)
        if level == 2:
            for name in ('tests', 'hack', 'regression'):
                binary = Path(temp) / name
                run(['gcc', '-std=c11', '-Wall', '-Wextra', '-Werror',
                     '-fsanitize=undefined', '-fno-sanitize-recover=all',
                     str(folder / f'{name}.c'), '-o', str(binary)], root)
                output = run([str(binary)], folder)
                if name == 'hack' and 'CONGRATULATIONS LEVEL 2 PASSED!' not in output:
                    raise SystemExit('C exploit still succeeds')
        else:
            run([sys.executable, 'tests.py'], folder)
            if level != 5:
                run([sys.executable, 'hack.py'], folder)
            run([sys.executable, 'regression.py'], folder)
        print(f'LEVEL {level}: PASS', flush=True)
    print('\nALL 5 SEASON 1 LEVELS: PASS', flush=True)
