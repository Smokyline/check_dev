# Указывает Docker использовать официальный образ python 3 с dockerhub в качестве базового образа
FROM python:3.10


#ENV DockerHOME=/web_django

# set work directory
#RUN mkdir -p $DockerHOME

# where your code lives
WORKDIR /window-edit

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install dependencies
RUN pip install --upgrade pip
# copy whole project to your docker home directory.
COPY requirements.txt ./
# run this command to install all dependencies
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]