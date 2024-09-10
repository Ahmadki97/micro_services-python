FROM python:3.11.4-alpine 

WORKDIR /usr/src/app

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# Prevent python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# ensure python output is sent directly to terminal 
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY 1-API_Gateway/packages.txt .

RUN pip install -r packages.txt

WORKDIR /usr/src/app/api_gateway

ENTRYPOINT ["python", "main.py"]

# ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]