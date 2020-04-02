There should be always a graphs of famous/important events in the world or your country in your local network/home/garage!

![Graph][logo]

Description: This script can run in almost any device that supports Python2 and has redis installed (it can work without redis too, if the telegram reporting is turned off). It runs in the background every 5 minutes via cron daemon and checks for new corona virus cases in the famous api (https://corona.lmao.ninja/countries/), collects information to the local rrdtool based databased, it draws nice rrdtool based graphical statistics in few images (metrics-daily.png  metrics-monthly.png  metrics-weekly.png) so you can implement in any html or program later. If you have some feature requests or just want to inform me about anything please write in the issues tab. Be safe, be smart, stay at home, and learn Unix! Visit us at http://www.unix-master.com/

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
