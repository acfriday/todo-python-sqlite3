FROM python:3.8-slim
RUN mkdir -p /app
COPY . /app/
WORKDIR /app/
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["python3", "app.py"]