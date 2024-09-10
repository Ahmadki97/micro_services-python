FROM python:3.11.4-alpine 

WORKDIR /usr/src/app

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# Prevent python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# ensure python output is sent directly to terminal 
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN pip install elasticsearch

RUN pip install flask

RUN pip install python-dotenv

RUN pip install pika

# ENTRYPOINT ["python", "app.py"]
ENTRYPOINT ["python", "app.py"]
# ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]