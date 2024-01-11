FROM python:3.8.8-slim

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app

RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

COPY . /usr/src/app

# RUN mkdir -p /opt/web/fastapi

CMD ["python3", "main.py"]
