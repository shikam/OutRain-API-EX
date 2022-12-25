FROM python:3.10
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
COPY ./input.json /code/input.json
RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt
COPY application /code/application
CMD ["python","application/API-Application.py","run","--host=0.0.0.0"]