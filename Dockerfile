FROM python:3.5
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ENV SECRET_KEY fakebuildkey

EXPOSE 8000

COPY bin/dumb-init /usr/local/bin/dumb-init
RUN chmod +x /usr/local/bin/dumb-init
ENTRYPOINT [ "/usr/local/bin/dumb-init", "--" ]

RUN mkdir /code
WORKDIR /code

# Production requirements
RUN pip install -U pip
ADD requirements.txt /
RUN pip install -r /requirements.txt --no-cache-dir --disable-pip-version-check

# Code
ADD .env /code/
ADD hostedfactor/ /code/
RUN ./manage.py collectstatic --noinput

