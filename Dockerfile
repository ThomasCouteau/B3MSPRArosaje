# specify the node base image with your desired version node:<version>
FROM node:16
# replace this with your application's default port
EXPOSE 8080
ENV container=docker
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y npm nodejs

COPY FRONT /home/node/app
WORKDIR /home/node/app

RUN npm install
RUN npm run start

FROM nginx
COPY --from=0 /home/node/app/dist/spa /usr/share/nginx/html
