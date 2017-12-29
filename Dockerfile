 FROM python:3
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /restaurant
 WORKDIR /restaurant
 ADD requirements.txt /restaurant/
 RUN pip install -r requirements.txt
 ADD . /restaurant/
