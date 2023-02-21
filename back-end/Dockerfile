FROM ubuntu:22.04
ENV container=docker
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    python3 \
    python3-pip \
    curl \
    && apt clean

COPY src /app

WORKDIR /app

RUN pip3 install -r requirements.txt

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl 0.0.0.0:8000/docs || exit 1

CMD ["python3", "app.py"]