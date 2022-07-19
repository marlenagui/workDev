from python:3.11.0b4-slim-bullseye

RUN mkdir /uploadFiles
WORKDIR /uploadFiles
# RUN mkdir static
# RUN mkdir templates

COPY requirements.txt /uploadFiles/
RUN pip3 install -r requirements.txt
copy uploadFiles.py /uploadFiles/

ADD static/ static/
ADD templates/ templates/

#ENTRYPOINT ["sh"]
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0" ]