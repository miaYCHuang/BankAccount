# Bank Account

> 實現銀行中使用者與銀行帳戶間的連結

透過[Swagger](http://34.81.137.177:3000/swagger/)可簡單得操作各項API，並與[資料庫](http://34.81.137.177:80/)聯動。
使用者名稱：root
密碼：12345678

## Getting Started 使用指南


### Prerequisites 使用條件

1. Linux環境(此處使用的是GCP Ubuntu20.04 LTS)
2. 安裝Docker
    * [下載Docker](https://docs.docker.com/engine/install/ubuntu/)
    * [Docker設置](https://docs.docker.com/engine/install/linux-postinstall/)
    * [下載Docker-Compose](https://docs.docker.com/compose/install/standalone/)

### Installation 安裝

建立Mysql備份文件:

```sh
mkdir mql
mkdir mql/initdb
mkdir mql/datadir
sudo apt install vim
vim mql/my.cnf
```

在my.cnf加入Mysql環境設定:
```sh
[client]
default_character_set=utf8
[mysqld]
collation_server = utf8_general_ci
character_set_server = utf8
```

下載docker-compose(可下載github上的):
```sh
wget "https://drive.google.com/u/0/uc?id=1ND8v728BU39A5TQ_qQvd0Vro-9DUMWvW&export=download" -O "docker-compose.yml"
```
