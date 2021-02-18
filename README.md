# Stock-Prediction
Analysis and Prediction of stocks using Machine Learning

## Initial Setup
### Install dependencies
```bash
$ curl https://pyenv.run | bash
$ sudo apt install -y libbz2-dev liblzma-dev

$ cd <dir>
$ gh repo clone sarthak7gupta/Stock-Prediction
$ cd Stock-Prediction

$ pyenv install 3.9.1
$ pyenv virtalenv 3.9.1 capstone
$ pyenv local capstone

$ pip install -U pip
$ pip install -r requirements.txt
```

### Run MongoDB and SQL locally. Reset required tables, files and directories
```bash
$ sudo docker run --name mongo -d -p 27017:27017 mongo
```

<table>
<tr>
<th> MySQL </th>
<th> Postgres SQL </th>
</tr>
<tr>
<td>

```bash
$ sudo apt install -y docker mysql-client
$ sudo docker run --name mysql -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_USER=root -e MYSQL_PASSWORD=root mysql/mysql-server
$ sudo docker exec -it mysql mysql -u root -p
> GRANT ALL ON *.* TO 'root'@'%' WITH GRANT OPTION;
> exit;
$ mysql -h 127.0.0.1 -P 3306 -u root -p
> exit;
$ export MYSQL_PASSWORD=root
```
</td>
<td>

```bash
$ sudo apt install -y postgresql-client
$ sudo docker run --name postgres -d -p 5432:5432 -e POSTGRES_PASSWORD=root -e POSTGRES_USER=root postgres
$ sudo docker exec -it postgres psql -h localhost -p 5432 -U root -W
$ psql -h localhost -p 5432 -U root -W
> exit;
$ export POSTGRES_PASSWORD=root
```
</td>
</tr>
</table>

```bash
$ python teardown.py
$ python setup.py
```

## Fetching data
<table>
<tr>
<th> StockPrice data </th>
<th> Articles data </th>
</tr>
<tr>
<td>

`$ python data_service.py`

#### Import from dump
`$ gunzip -c database/dump.sql.gz | mysql -h 127.0.0.1 -P 3306 -u root -D capstone -p`
#### Export to dump
`$ mysqldump -h 127.0.0.1 -P 3306 -u root -p capstone | gzip > database/dump.sql.gz`

</td>
<td>

`$ python article_service.py`
#### Import from dump
`$ mongorestore --db=capstone --archive=database/dump.nosql.gz --gzip`
#### Export to dump
`$ mongodump --forceTableScan --db=capstone --archive=database/dump.nosql.gz --gzip`
</td>
</tr>
</table>
