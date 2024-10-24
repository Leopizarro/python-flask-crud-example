FROM python:3

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "flask", "--app", "flaskr", "run", "--debug", "--host=0.0.0.0"]