FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install sqlalchemy
RUN pip install pymysql
RUN pip install cryptography

COPY . .

EXPOSE 8080
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port","8080"]