FROM ubuntu:20.04
LABEL app="elq"

ENV TZ=Europe/Moscow
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
&& apt-get update \
&& apt-get install -y \
  sudo \
  nano \
  whois \
  usbutils \
  cups \
  cups-client \
  cups-bsd \
  cups-filters \
  foomatic-db-compressed-ppds \
  printer-driver-all \
  openprinting-ppds \
  smbclient \
  git \
  gcc \
  python3-pip \
  libcups2-dev \
  python3-dev \
  python3-setuptools

# Add user and disable sudo password checking
RUN useradd \
  --groups=sudo,lp,lpadmin \
  --create-home \
  --home-dir=/home/print \
  --shell=/bin/bash \
  --password=$(mkpasswd print) \
  print \
&& sed -i '/%sudo[[:space:]]/ s/ALL[[:space:]]*$/NOPASSWD:ALL/' /etc/sudoers

# CUPS - Copy the default configuration file
COPY --chown=root:lp cupsd.conf /etc/cups/cupsd.conf
COPY --chown=root:root RasterToSPrinter /usr/lib/cups/filter/RasterToSPrinter
RUN chmod 755 /usr/lib/cups/filter/RasterToSPrinter 
# Deploy django app
RUN git clone https://github.com/MyEternityOrg/elq.git && cd elq && pip3 install -r requirements.txt
COPY .env /app/elq
RUN cd elq && python3 manage.py migrate && python3 manage.py init

EXPOSE 8000
EXPOSE 631
CMD cd elq && git pull origin master && service cups restart && python3 manage.py runserver 0.0.0.0:8000