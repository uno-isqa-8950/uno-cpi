import sys
import subprocess

# implement conda as a subprocess:

subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                       'python3-saml'])

subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                       '--force-reinstall', '--use-pep517', 'lxml', 'lxml'])

subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                       '-r', 'UnoCPI/requirements.txt'])
