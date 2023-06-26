FROM python:alpine

LABEL version="0.0.1"
LABEL description="Instagram automation."

WORKDIR /app
COPY . /app
VOLUME [ "/app/logs" ]
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python3", "/app/main.py" ]
ENV IG_USERNAME=""
ENV IG_PASSWORD=""