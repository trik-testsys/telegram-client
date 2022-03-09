FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH="$PYTHONPATH:/bot"
CMD [ "python3","bot/main.py3" ]
