FROM python:3.6.3

ENV SLACK_T1 xoxb-1425337867252-141249
ENV SLACK_T2 5700022-jVHglEbfTtfhfPVcSQpOsPS9
ENV SLACK_S1 1dd372d0d63b8
ENV SLACK_S2 ef38b7733535a759489
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
ENV PYTHONUNBUFFERED=1
WORKDIR /nestor_slack_reader_2
COPY ./nestor_slack_reader_2.py /nestor_slack_reader_2.py
CMD ["python", "/nestor_slack_reader_2.py"]