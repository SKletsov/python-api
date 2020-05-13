docker build -t mysyslog .
docker run  -d --cap-add SYSLOG --restart always -v /var/log:/var/log -p 514:514 -p 514:514/udp --name rsyslog mysyslog