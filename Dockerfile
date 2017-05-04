FROM python:3.5.3
ARG db_pass
ENV DB_PASSWORD $db_pass
WORKDIR /code
COPY . /code
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    postgresql-client \ 
    && rm -rf /var/lib/apt/lists/*
RUN /code/setup.sh
EXPOSE 8000
CMD ["sh", "start.sh"]


