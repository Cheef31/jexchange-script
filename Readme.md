## Start Bot
```shell
sudo crontab -e
* * * * * python3 /home/cheef/Git/waleed/jexchange-script/main.py
* * * * * ( sleep 10 ; python3 /home/cheef/Git/waleed/jexchange-script/main.py)
* * * * * ( sleep 20 ; python3 /home/cheef/Git/waleed/jexchange-script/main.py)
* * * * * ( sleep 30 ; python3 /home/cheef/Git/waleed/jexchange-script/main.py)
* * * * * ( sleep 40 ; python3 /home/cheef/Git/waleed/jexchange-script/main.py)
* * * * * ( sleep 50 ; python3 /home/cheef/Git/waleed/jexchange-script/main.py)
```