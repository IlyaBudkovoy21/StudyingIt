FROM python:3.12.2
RUN pip install --upgrade pip
WORKDIR /back
COPY . .
RUN pip install -r requirements.txt
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "StudyingIt.wsgi:application"]