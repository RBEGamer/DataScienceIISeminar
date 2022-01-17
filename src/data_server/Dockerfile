FROM tiangolo/uwsgi-nginx-flask:python3.9

RUN apt update && apt upgrade -y && apt install python3-pip python3-dev -y
#RUN apk --update add bash nano
WORKDIR /usr/src/app

COPY . .
EXPOSE 3017
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]