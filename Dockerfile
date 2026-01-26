FROM python:3.9-slim
WORKDIR /var/www/html
COPY ./output/ .
EXPOSE 80
CMD ["python", "-m", "http.server", "80"]
