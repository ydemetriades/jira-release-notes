FROM python:3.6.4-alpine3.7
LABEL maintainer="yiannis.demetriades@gmail.com"

ENV LANG C.UTF-8

RUN apk update && \
    apk upgrade && \
    pip install --no-cache-dir requests argparse

COPY script/jira-release-notes.py /jira-release-notes.py

ENTRYPOINT ["python", "/jira-release-notes.py"]