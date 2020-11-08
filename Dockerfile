FROM tiangolo/uwsgi-nginx-flask:python3.8
RUN pip3 install psycopg2
COPY ./app /app
