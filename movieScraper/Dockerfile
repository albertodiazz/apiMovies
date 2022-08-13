FROM 'python:3.10.5-alpine'
RUN apk --no-cache add curl
RUN mkdir app/
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/
