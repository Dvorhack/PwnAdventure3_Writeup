# Proxy

The proxy allows you to see the packets sent to and from the server.

The most known packets will be displayed with the name of the field and the unknown packets are just displayed as hex.

## Usage:
Put the ip of the computer which will run the proxy in the local DNS of your computer:
- edit `/etc/hosts` on Linux / Mac `C:\Windows\System32\Drivers\etc\hosts`
- add the following lines:
```
<ip> game.pwn3
<ip> master_docker.pwn3
```
With `<ip>` the ip of the proxy

Run the proxy with python 3: `python3 proxy.py`

Enjoy your proxy :)