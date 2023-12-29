FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app


RUN apt update && apt install -y g++ libpq-dev gcc musl-dev  \
    libssl-dev libffi-dev && apt clean

COPY requirements.txt .

RUN python3 -m pip install --no-compile -r requirements.txt

COPY . .

RUN apt remove -y --purge gcc g++ && apt autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/www/sheltuz

CMD ["./run.sh"]
