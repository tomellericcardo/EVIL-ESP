# EVIL-ESP :smiling_imp:
A super portable evil device, based on the ESP8266 board, running Micropython and equipped with a single button and a small OLED display.

## Attacks :hocho:
At the moment, it is able to perform three attacks:

- **Beacon Spammer**: it spams multiple WiFi beacons to make appear many fake access points on the nearby devices :mega:

- **Captive Portal**: it creates a "free hotspot" and redirects the users to a registration page, where they - hopefully - enter their usual email/password combination. Anyway, it never makes them sign in :sweat_smile:

- **Evil Twin**: it looks for nearby protected networks and lets you select the target one, then it sets up an open access point with the same ESSID of the victim and it uses a captive portal to redirect the users to a page which requires the WiFi password "in order to complete the firmware upgrade" :innocent:

## Logs :page_with_curl:
The credentials retrieved by both attacks are saved to a dedicated file: `data/captive_portal/log.csv` and `data/evil_twin/log.csv`. They can be viewed directly from the device, and they are also printed at startup on the Micropython console.

## Installation :wrench:
It takes just a few steps to set it up:

- Connect an i2c OLED display and a push button (to a pin which provides a pull-up resistor)
- Flash the Micropython firmware provided in the `firmware/` folder
- Edit the `data/config.json` file to match your hardware configuration and satisfy your preferences
- Upload the project tree to your device (using `ampy` or any similar tool)

You may eventually want to use an external antenna to boost your signal, but it is not required. To make it portable, you can use li-po battery or more simply a power bank.

### Headless setup
You can also setup your board to work without the hardware interface. Just edit the configuration file and disable the display or the button (or both) and specify the attack you want to perform at startup

Note that if you want to perform the evil twin attack using the headless seup, you also need to specify the SSID of the target access point in the configuration file.

## About deauthentication :syringe:
Usually, when performing an evil twin attack, you may want to send deauthentication frames to the target and its users, in order to make them connect to your malicious access point.
Unfortunately, Micropython doesn't provide a function which lets you send 802.11 raw packets, but even if it's possible to expose the `wifi_send_pkt_freedom` function to the network module (as I did to add the *Beacon Spammer* attack option), that function prevents the transmission of management frames such as deauthentication and disassociation after the version 1.3 of the Espressif SDK :man_facepalming:

Maybe one day I will try to build Micropython using that old SDK, but until then, you can easily do this **super dangerous action** with any PC running Linux, so have fun!

## Coming soon :hourglass:
- Add a configuration mode, to change the settings on the go
