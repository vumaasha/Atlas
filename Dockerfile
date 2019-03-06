# reference: https://hub.docker.com/_/ubuntu/
FROM ubuntu:latest

# Adds metadata to the image as a key value pair example LABEL version="1.0"
LABEL maintainer="Girish Shanmugam <s.girishshanmugam@gmail.com>"


# install Ubuntu dependencies and python image
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev git \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip


# Clone git repository and install requirements
RUN git clone https://github.com/vumaasha/Atlas.git \
	&& pip3 install -r Atlas/models/product_categorization/requirements.txt
