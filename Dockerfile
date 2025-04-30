FROM python:3.12.2
RUN pip install --upgrade pip
COPY src/ .
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["gunicorn", "StudyingIt.wsgi:application", "--bind", "0.0.0.0:8000"]