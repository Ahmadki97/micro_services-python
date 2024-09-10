FROM python


WORKDIR /usr/src/app

RUN apt update && apt install -y gcc python3-dev musl-dev default-libmysqlclient-dev build-essential

# Prevent python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# ensure python output is sent directly to terminal 
ENV PYTHONUNBUFFERED 1

COPY 3-Authentication_Service/auth/packages.txt .

RUN pip install --upgrade pip

RUN pip install -r packages.txt



# COPY User_Service/user_serv/requirements.txt .

# RUN pip install -r requirements.txt

# COPY entrypoint.sh .


# RUN chmod +x entrypoint.sh

ENTRYPOINT ["python", "app.py"]

# ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]