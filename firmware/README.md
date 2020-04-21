# About this firmware
This firmware is a custom build of Micropython which exposes the `wifi_send_pkt_freedom` function to the network module. See [this post](https://forum.micropython.org/viewtopic.php?t=3389) if you want to build it yourself.

## Usage
You need to setup a station interface and then call the `freedom` function to send the frame to a specific channel:

```python
import network

sta = network.WLAN(network.STA_IF)
sta.active(True)

sta.freedom(channel, packet)
```
