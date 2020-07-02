#!/usr/bin/env python3

import finnhub
import rainbowhat as rh
import time
import os
from dotenv import load_dotenv

load_dotenv()

LED_BRIGHTNESS = 0.2
LED_COLOR_PEAK = 10
DISPLAY_SPEED = 0.3
STOCK_LIST = ["GOOG", "INTC", "MSFT", "FB", "PYPL", "AAPL"]
STOCK_POINTER = 0

configuration = finnhub.Configuration(
    api_key={
        'token': os.getenv("FINNHUB_TOKEN")
    })

finnhub_client = finnhub.DefaultApi(finnhub.ApiClient(configuration))


def findDotsInString(str):
    dotLocation = []
    i = 0
    for idx in range(len(str)):
        if str[idx] == '.':
            dotLocation.append(idx - 1 - i)
            i += 1
    return dotLocation


def resetAlldots():
    for id in range(0, 4):
        rh.display.set_decimal(id, False)
        rh.display.show()


def stockTrend(current_price, previous_close):
    stock_trend = "+"
    if current_price < previous_close:
        stock_trend = "-"
    return stock_trend


def showLedBasedOnPercentage(percentage):
    led_numbers = percentage

    if led_numbers > 7:
        led_numbers = 7
    rh.rainbow.clear()

    for x in range(int(led_numbers)):
        if stock_trend == "+":
            rh.rainbow.set_pixel(6 - x,
                                 0,
                                 LED_COLOR_PEAK,
                                 0,
                                 brightness=LED_BRIGHTNESS)
        else:
            rh.rainbow.set_pixel(6 - x,
                                 LED_COLOR_PEAK,
                                 0,
                                 0,
                                 brightness=LED_BRIGHTNESS)
    rh.rainbow.show()


def incrementStockPointer():
    global STOCK_POINTER
    STOCK_POINTER += 1
    STOCK_POINTER = STOCK_POINTER % len(STOCK_LIST)


while True:
    try:
        stockName = STOCK_LIST[STOCK_POINTER]
        # Fetches Stock Data
        stockData = finnhub_client.quote(stockName)
        previous_close = stockData.pc
        current_price = stockData.c
        stock_trend = stockTrend(current_price, previous_close)
        percentage = ((current_price - previous_close) / previous_close) * 100

        percentage = abs(float("{:.2f}".format(percentage)))
        display_string = "   "+stockName + " " + \
            str(current_price) + " " + stock_trend + str(percentage) + "%     "
        dotPosition = findDotsInString(display_string)

        showLedBasedOnPercentage(percentage)
        print(display_string)

        display_string = display_string.replace(".", "")

        for element in range(0, (len(display_string) - 4)):
            rh.display.print_str(display_string[element] +
                                 display_string[element + 1] +
                                 display_string[element + 2] +
                                 display_string[element + 3])
            rh.display.show()
            resetAlldots()

            for i in range(0, 4):
                if (element + i in dotPosition):
                    rh.display.set_decimal(i, True)

            rh.display.show()
            time.sleep(DISPLAY_SPEED)

        incrementStockPointer()
    except:
        rh.display.print_str("ERRR")
        rh.display.show()
        rh.rainbow.set_all(LED_COLOR_PEAK, 0, 0, brightness=LED_BRIGHTNESS)
        rh.rainbow.show()
        incrementStockPointer()
        time.sleep(3)
