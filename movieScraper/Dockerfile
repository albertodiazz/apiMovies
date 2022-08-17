FROM 'python:3.10.5-alpine'
# Esto nos sirve para hacer uso de curl dentro de nuestra API
RUN apk --no-cache add curl
RUN mkdir app/
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/
