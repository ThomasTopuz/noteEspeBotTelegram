FROM python:3
WORKDIR /app
ENV PORT=8443
COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "main.py"]
