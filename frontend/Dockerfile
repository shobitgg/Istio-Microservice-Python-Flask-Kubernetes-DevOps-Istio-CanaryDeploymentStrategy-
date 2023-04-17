FROM python:3.9
ENV SERVER_IP="0.0.0.0"
ENV SERVER_PORT="5000"
COPY .  /app/
WORKDIR /app
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y vim && chmod -R 777 /opt
CMD ["python", "app.py"]
