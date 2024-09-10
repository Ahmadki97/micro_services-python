FROM python

WORKDIR /usr/src/app/

RUN apt update && apt install -y gcc python3-dev musl-dev default-libmysqlclient-dev build-essential

# Prevent python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# ensure python output is sent directly to terminal 
ENV PYTHONUNBUFFERED 1

COPY 6-Chat_Service/Chat/packages.txt .

RUN pip install --upgrade pip

RUN pip install -r packages.txt


WORKDIR /usr/src/app/Source


ENTRYPOINT ["python", "main.py"]