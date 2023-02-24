FROM ubuntu:22.04
ENV container=docker
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y npm nodejs

COPY FRONT /app
WORKDIR /app

RUN npm install

HEALTHCHECK --interval=30s --timeout=30s --start-period=20s --retries=3 CMD curl -f http://localhost:8080/ || exit 1

CMD ["npm","run", "start"]