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

$ pyenv install 3.8.6
$ pyenv virtalenv 3.8.6 capstone
$ pyenv local capstone

$ pip install -U pip
$ pip install -r requirements.txt
```

### Setup databases, folders and directories
```bash
$ export <MYSQL|POSTGRES>_PASSWORD=<password>

$ ./term_db.sh
$ ./init_db.sh [MYSQL|POSTGRES]
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
