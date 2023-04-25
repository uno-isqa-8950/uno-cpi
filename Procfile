web: gunicorn UnoCPI.wsgi --log-file -
jobs: python jobs.py
build: pip install python3-saml && pip install --force-reinstall --use-pep517 lxml lxml && pip install -r requirements.txt
