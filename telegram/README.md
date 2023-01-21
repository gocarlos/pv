# Telegram Bot

Öffne den Chat mit dem User 'BotFather'

![BotFather](https://github.com/thomhug/pv/blob/main/telegram/img/Screenshot%202023-01-21%20at%2020.59.53.png)

Schreibe /newbot

Folge den Anweisungen bis du das HTTP API Token hast.

Füge das Token in das [echo_bot.py](https://github.com/thomhug/pv/blob/main/telegram/echo_bot.py) Skript und starte es.

Gehe auf deinen Bot (klicke auf den Link in der Message vom BotFather) und schreibe ihm etwas. 

```
$ ./echo_bot.py 

Bot started...

Id: 371813964 - hi
^C
```

Das [echo_bot.py](https://github.com/thomhug/pv/blob/main/telegram/echo_bot.py) Skript gibt nun eine Nummer aus. Das ist die Id von deinem User.

Jetzt kannst du diese Nummer und das Token in tg-bot-test einfüllen und das Skript laufen lassen.

![solarbot](https://github.com/thomhug/pv/blob/main/telegram/img/Screenshot%202023-01-21%20at%2022.02.58.png)

Willkommen bei den unbegrenzten Möglichkeiten von Telegram Bots! Lade den Bot in eine Gruppe ein und erlaube ihm alle Mitteilungen zu lesen, indem du ihn zum Admin machst. Ich habe das gemacht mit dieser (öffentlichen) Gruppe: [https://t.me/solarprognose](https://t.me/solarprognose).

Das Skript tg-solar-notify (Token und Gruppen-Nr. anpassen - deine Gruppennummer bekommst du, wenn du in der Gruppe, in der du den Bot zum Admin gemacht hast, etwas schreibst und mit dem [echo_bot.py](https://github.com/thomhug/pv/blob/main/telegram/echo_bot.py) mithörst. Gruppennummern sind negativ) ruft ein weiteres Skript solar-prognose auf und schickt deren Inhalt in die Gruppe. Du kannst den Output natürlich auch nur in der Direktmessage mit dem Bot schicken.