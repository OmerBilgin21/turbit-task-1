FROM python:3.10-slim

WORKDIR /app
COPY . /app/
RUN pip3 install -r requirements.txt

RUN chmod +x /app/wait-for-it.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]


