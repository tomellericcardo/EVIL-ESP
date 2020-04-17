# EVIL-ESP :smiling_imp:
A super portable evil device, based on the ESP8266 board, running Micropython and equipped with a single button and a small OLED display.

## Attacks :hocho:
At the moment, it is able to perform two social engineering attacks:

- **Captive Portal**: it creates a "free hotspot" and redirects the users to a registration page, where they - hopefully - enter their usual email/password combination. Anyway, it never makes them sign in :sweat_smile:

- **Evil Twin**: it looks for nearby protected networks and lets you select the target one, then it sets up an open access point with the same ESSID of the victim and it uses a captive portal to redirect the users to a page which requires the WiFi password "in order to complete the firmware upgrade" :innocent:

## Logs :page_with_curl:
The credentials retrieved by both attacks are saved to a dedicated file: `data/captive_portal/log.csv` and `data/evil_twin/log.csv`. They can be viewed directly from the device, and they are also printed at startup on the Micropython console.

## Installation :wrench:
It takes just a few steps to set it up:

- Connect an i2c OLED display and a push button (to a pin which provides a pull-up resistor)
- Flash the latest Micropython firmware (I only tested it with v1.12)
- Edit the `data/config.json` file to match your hardware configuration and satisfy your preferences
- Upload the project tree to your device (using `ampy` or any similar tool)

You may eventually want to use an external antenna to boost your signal, but it is not required. To make it portable, you can use li-po battery or more simply a power bank.

## About deauthentication :syringe:
Usually, when performing an evil twin attack, you may want to send deauthentication frames to the target and its users, in order to make them connect to your malicious access point.
Unfortunately, Micropython doesn't provide a function which lets you send 802.11 raw packets, but even if someone managed to expose the `wifi_send_pkt_freedom` to the network module (see [this post](https://forum.micropython.org/viewtopic.php?t=3389)), the function prevents the transmission of any management frame (including deauthentication and disassociation) after the version 1.3 of the Espressif SDK, for security reasons :man_facepalming:

Maybe one day I will try to build Micropython using that old SDK, but until then, you can easily do this **super dangerous action** with any PC running Linux, so have fun!

## Coming soon :hourglass:
- Add a configuration mode, to change the settings on the go
- Add a beacon functionality, to spam fake APs
