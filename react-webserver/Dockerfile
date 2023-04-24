# pull official base image
FROM node:alpine

# Install python/pip
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

# Install bash
RUN apk add --no-cache bash

# install app dependencies
COPY package.json /

# add app
COPY public /public/
COPY src /src/
COPY tmp /tmp/
ADD .env /.env

# add start function
ADD start_server.sh /start_server.sh
RUN chmod +x /start_server.sh

# run npm install / update / build
RUN npm install
RUN npm update
RUN npm run build
RUN npm install -g serve

# expose port
EXPOSE 443:443
EXPOSE 80:80

# start app
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["./start_server.sh"]
