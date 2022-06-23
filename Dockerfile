FROM python

WORKDIR /main
COPY requirements.txt /main
RUN pip install -r requirements.txt

