FROM python:3.9-slim

ADD requirements.txt /app/
RUN pip3 install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/ \
    && pip3 install -r /app/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

ADD . /app
WORKDIR /app

EXPOSE 8000
CMD ["uvicorn", "controller:app", "--host", "0.0.0.0", "--port", "8000"]