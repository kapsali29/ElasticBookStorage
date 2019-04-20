## ElasticBookStorage

This is a Python project that uses Elastic search to do some basic operations

### Requirements

+ Operating System: Ubuntu 16x, 17x, 18x
+ Programming Language: Python 3x
+ elasticsearch==7.0.0
+ urllib3==1.24.2

### Docker installation

```
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get -y install docker-ce
```

### docker-compose installation

```
sudo curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Install ElasticSearch & Kibana

```
sudo docker-compose -f modules/docker-compose.yml up -d
```