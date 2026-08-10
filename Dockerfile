# Python 3.11 to match the other three services in the stack.
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# mysqlclient 2.2.7 has no manylinux wheel, so it compiles from source and
# needs a C toolchain plus the MySQL client headers.
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        default-libmysqlclient-dev \
        default-mysql-client \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.docker.txt /app/requirements.docker.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.docker.txt

COPY . /app

# settings.py opens 'credentials.yaml' by a CWD-relative path, so the working
# directory has to be the one holding it -- /app, alongside manage.py.

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
