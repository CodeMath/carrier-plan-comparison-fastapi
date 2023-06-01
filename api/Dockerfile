FROM python:3.9

WORKDIR /app

ADD requirements.txt /app/
RUN pip install --no-cache-dir --upgrade -r requirements.txt
ADD . /app/

# EXPOSE 8080
# CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8080", "main:app"]