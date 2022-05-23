FROM python:3.9

RUN mkdir -p /app
WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY ./app/app.py ./app.py

# EXPOSE 8050
# CMD python app.py

EXPOSE 4000
CMD gunicorn -b 0.0.0.0:4000 app:server
