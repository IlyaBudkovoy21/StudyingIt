FROM python:3.12.2
RUN pip install --upgrade pip
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]