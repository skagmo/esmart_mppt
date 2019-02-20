# eSmart 3 python library

Python 3 library to communicate with the eSmart3 MPPT charger, [as reviewed here.](http://skagmo.com/page.php?p=documents%2F04_esmart3_review)

* esmart.py: Library
* esmart_test.py: Example/test using the library

You need an RS-485 adapter to communicate with the device, [like this one.](https://www.aliexpress.com/item/USB-2-0-to-TTL-RS485-Serial-Converter-Adapter-FTDI-Module-FT232RL-SN75176-double-function-double/32687049767.html)

RJ45 pinout:
* 1: A
* 2: B
* 5,6: Ground
* 7,8: 5V out (for powering isolated RS-485 interface)
