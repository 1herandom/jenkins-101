FROM python:3.10-slim
WORKDIR /usr/local/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "hello.py"]

