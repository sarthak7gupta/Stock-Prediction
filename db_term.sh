#!/bin/bash

sudo docker stop postgres
sudo docker stop mysql
sudo docker stop mongo
yes | sudo docker system prune
yes | sudo docker volume prune
