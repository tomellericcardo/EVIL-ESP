# ESP8266 Deauther
If you want to deuthenticate nearby devices to make a complete evil twin attack or if you just want to have a WiFi pseudo-jammer, you can use this Arduino sketch.

## Installation
In order to compile and flash this sketch on your ESP8266, you need to use a specific SDK for Arduino: the [Arduino core for ESP8266 Deauther](https://github.com/tobozo/Arduino). The IDE configuration is easy and well described on the [README](https://github.com/tobozo/Arduino/blob/deauther/README.md#installation).

## Usage
At the moment, this program works fine with a headless setup: when powering up the device, it will scan nearby networks and it will look for two access points with the same SSID. In that case, it will start to deauthenticate all client devices of the protected one (so it's easy to use alongside your main device performing an evil twin attack).

If it can't find any duplicated access point within a minute, it will start to deauthenticate all networks.

## To do
- Log target devices and deauthentication frames counter
