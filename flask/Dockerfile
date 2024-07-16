FROM python:3.12

ARG project_dir=/flask/

ADD ./requirements.txt $project_dir

WORKDIR $project_dir

RUN pip install -r requirements.txt
