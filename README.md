# Stock-Prediction
Analysis and Prediction of stocks using Machine Learning

## Initial Setup
### Install pyenv, compile & install Python with required libraries, and create virtual environment and install requirements
```
curl https://pyenv.run | bash
sudo apt install -y libbz2-dev liblzma-dev

pyenv install 3.9.1
pyenv virtalenv 3.9.1 capstone
pyenv local capstone

cd
gh repo clone sarthak7gupta/Stock-Prediction
cd Stock-Prediction

pip install -U pip
pip install -r requirements.txt

sudo apt install -y docker mysql-client
```

### Run MongoDB and MySQL locally. Create required tables and directories with setup.py
```
sudo docker run --name mongo -d -p 27017:27017 mongo
sudo docker run --name mysql -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_USER=root -e MYSQL_PASSWORD=root mysql/mysql-server
sudo docker exec -it mysql mysql -u root -p
GRANT ALL ON *.* TO 'root'@'%' WITH GRANT OPTION;
exit;
mysql -h 127.0.0.1 -P 3306 -u root -p
exit;

export MYSQL_PASSWORD=root
python teardown.py
python setup.py
```

## Get Stock Price data manually and store in db
```
python data_service.py  # or Import from dump: gunzip database/dump.sql.gz; cat database/dump.sql | mysql -h 127.0.0.1 -P 3306 -u root -D capstone -p
```
