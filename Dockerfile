FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install whitenoise

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "otzovik.wsgi:application"]
