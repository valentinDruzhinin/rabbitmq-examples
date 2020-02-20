FROM python:3.7
ADD . /rabbit-test-app
WORKDIR /rabbit-test-app
RUN pip install -r requirements.txt
CMD python send.py