<div style="text-align:center"><img alt="StockPi Logo" src="./docs/logo.png" /></div>

StockPi is a RaspberryPi based real-time stock price monitoring system powered by [Finnhub's API](https://finnhub.io/)

## Motivation

I am a huge stock market enthusiast and monitoring stock prices in realtime requires a dedicated device. So I decided to make it fun and intuitive by using a Raspberry Pi rusting in my cupboard :)

![Demo Gif](./docs/demo.gif)

## Getting up and running

### Hardware

- RaspbeeryPi 3 or above.
- [Rainbow HAT](https://shop.pimoroni.com/products/rainbow-hat-for-android-things)
- Micro USB adapter (Old mobile phone charger).

### Software

- RasbianOS or something similar
- Python3
- [rainboaw-hat (Python)](https://github.com/pimoroni/rainbow-hat)
- Finnhub API Token

---

### Let's get this started

Clone the repo

```
git clone https://github.com/pranshuchittora/stockpi.git
```

Install the dependencies

```bash
 pip3 install -r requirements.txt
```

Setup Finnhub account and generate API token. Copy and paste the token in the `.env` file.

```.env
FINNHUB_TOKEN='FINNHUB_API_TOKEN'
```

Run `main.py`

```bash
python3 main.py
```

**Voilla 🤗**

## Service setup on system startup (MacOS/Linux only)

Main advantages of running this on Raspberry Pi is that it's a low power device and we can configure it to auto-run the script on startup which makes it hassle-free.

Change file permissions

```bash
chmod u+x main.py
```

### Create a system service

Run the following command to create a service

```
> sudo systemctl edit --force --full stockpi.service
```

Insert these statements with your settings, save them and quit the editor

```
[Unit]
Description=StockPi Service
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/stockpi
ExecStart=/home/pi/stockpi/main.py

[Install]
WantedBy=multi-user.target
```

Run `systemctl status stockpi.service` to get the service status

```
> systemctl status stockpi.service

● stockpi.service - StockPi Service
    Loaded: loaded (/etc/systemd/system/stockpi.service; disabled; vendor preset: enabled)
    Active: inactive (dead)
```

Now let's enable and start the service

```
> sudo systemctl enable stockpi.service
> sudo systemctl start stockpi.service
```

Yaaay, now to don't need to start the program manually. I'm not a robot 🤖
