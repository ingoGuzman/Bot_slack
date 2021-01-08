FROM python:3.6.3

ENV SLACK_T1 xoxb-1425337867252-141249
ENV SLACK_T2 5700022-jVHglEbfTtfhfPVcSQpOsPS9

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

WORKDIR /nestor_slack_writer

COPY ./nestor_slack_writer.py /nestor_slack_writer.py

CMD ["python", "/nestor_slack_writer.py"]