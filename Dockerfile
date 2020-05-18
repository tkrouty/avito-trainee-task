FROM python:3.7

RUN mkdir /source
WORKDIR /source
COPY . /source
RUN pip install -r requirements.txt
EXPOSE 8000
