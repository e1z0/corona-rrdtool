There should be always a graphs of famous/important events in the world or your country in your local network/home/garage!

![Graph][logo]

## Install deps: 
``
apt install python-rrdtool python-redis python-json python-requests
``

## Install script

copy it to /usr/local/bin/, then set the permissions
```
chmod +x /usr/local/bin/corona.py
```

Edit script parameters inside script:
```
api = 'https://corona.lmao.ninja/countries/'
country = 'LT'
html_dir = '/var/www/html/corona/'
report_telegram = 1
tg_bot = "create_bot_and_copy_text_after_bot_string"
```

Check if it works
```
./corona.py 
```


## Use in crontab:
```
*/5 * * * * root <path>/corona.py --update
*/10 * * * * root <path>/corona.py --graph
```


[logo]: https://raw.githubusercontent.com/e1z0/corona-rrdtool/master/img/metrics-daily.png
