FROM python:3
ENV PYTHONUNBUFFERED=1
RUN mkdir /myCode
WORKDIR /myCode
COPY requirements.txt /myCode/
RUN pip install -r requirements.txt
COPY . /myCode/
