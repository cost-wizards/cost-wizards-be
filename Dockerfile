FROM python:3.10

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install .
RUN apt-get update -y && \
    apt-get install -y  build-essential nginx python3-pip python3-dev  supervisor \
    libpq-dev postgresql postgresql-contrib libldap2-dev libsasl2-dev freetds-dev uwsgi-plugin-python3 redis-server -y && \
    pip install -r requirements.txt --no-cache-dir && \
    apt install -y awscli && \
    apt-get install -y curl && \
    apt-get install -y wget && \
    wget https://truststore.pki.rds.amazonaws.com/us-east-1/us-east-1-bundle.pem && \
    curl -sf https://raw.githubusercontent.com/pratishshr/envault/master/install.sh | sh
# copy project
COPY . .
RUN chmod +x run_server.sh

CMD [ "./run_server.sh" ]