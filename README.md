# Bank Account

> 實現銀行中使用者與銀行帳戶間的連結

透過[Swagger](http://34.81.137.177:3000/swagger/)可簡單的操作各項API並與[資料庫](http://34.81.137.177:80/)連動。


## Getting Started 使用指南


### Prerequisites 使用條件

1. Linux環境(例如:GCP Ubuntu20.04 LTS)
2. 安裝Docker
   2-1. 參考官網
   
    * [下載Docker](https://docs.docker.com/engine/install/ubuntu/)
    * [Docker設置](https://docs.docker.com/engine/install/linux-postinstall/)
    * [下載Docker-Compose](https://docs.docker.com/compose/install/standalone/)
   2-2. 執行Shell Script
    * [下載](https://drive.google.com/drive/folders/1z7FMeGuAgzjEBOxhyFUDH1iBzzcbbbDH?usp=sharing)
    ```sh
chmod +x ./*
./installDocker.sh
./without_sudo.sh
./installDockerCompose.sh
   ```

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

查看目錄路徑:

```sh
pwd
```

修改docker-compose裡pythonAPI的Volume位置:

```sh
vim docker-compose.yml
```

```sh
      - /home/需修改/mql/initdb:/docker-entrypoint-initdb.d
      - /home/需修改/mql/datadir:/var/lib/mysql
      - /home/需修改/mql/my.cnf:/etc/mysql/conf.d/my.cnf
```

---
#### #下載AWS上的image需執行以下步驟
```sh
      image: 625565224680.dkr.ecr.ap-southeast-2.amazonaws.com/api:1.2
```

安裝AWS:
```sh
sudo apt install awscli
aws configure
```
aws configure為(需要請與我聯繫):
```sh
存取金鑰
私密存取金鑰
空格
空格
```

擷取驗證字符並將 Docker 用戶端驗證至您的登錄檔。
使用 AWS CLI：:
```sh
aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 625565224680.dkr.ecr.ap-southeast-2.amazonaws.com
```
---
建立docker-compose:
```sh
docker-compose up -d
```



### Usage example 使用範例
IP需替換成自己環境的IP


資料庫為：http://34.81.137.177:80/


    * 使用者名稱：root
    * 密碼：12345678
    * 匯入資料表，在github裡的BankAccount/mysql/api_accounts.sql與api_users.sql

API測試：http://34.81.137.177:3000/


API測試(資料庫)：http://34.81.137.177:3000/test


API範例(Swagger)：http://34.81.137.177:3000/swagger/

---
#### #使用GCP需至防火牆設定


port:80(勾選Http則無需再加入)


port:3000


---
