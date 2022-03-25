FROM python:3.9

WORKDIR /awesomechecker-bot

COPY ./src ./src

RUN pip install -r ./src/requirements.txt

WORKDIR /awesomechecker-bot/src

CMD [ "python", "main.py" ]