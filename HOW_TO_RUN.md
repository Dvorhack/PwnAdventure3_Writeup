# Install the dependencies
## Ubuntu
Then, you must install libssl1.0 `http://archive.ubuntu.com/ubuntu/pool/main/o/openssl1.0/libssl1.0.0_1.0.2n-1ubuntu5_amd64.deb`.  
And install it `sudo apt install ./libssl1.0.0_1.0.2n-1ubuntu5_amd64.deb`


## Arch
comming soon


# Run the game
Download the game binary `https://www.pwnadventure.com/PwnAdventure3_Linux.zip`

Edit the file `PwnAdventure3/PwnAdventure3/Content/Server/server.ini` and write:
```
[MasterServer]
Hostname=master_docker.pwn3
Port=3333

[GameServer]
Hostname=game.pwn3
Port=3000
Username=Pvl
Password=azerty
```

## Linux
Add the ip of the server to you `/etc/hosts`
```
20.111.26.84 game.pwn3
20.111.26.84 master_docker.pwn3
```

Set your keyboard un us: `setxkbmap us`

In order to run the game, you must cd to the binary folder `cd PwnAdventure3/Binaries/Linux`.  
And you can run it `PwnAdventure3-Linux-Shipping`

## Windows
Open notepad as administrator and edit the file `C:\windows\system32\drivers\etc\hosts`.  
Add the following lines
```
20.111.26.84 game.pwn3
20.111.26.84 master_docker.pwn3
```

Run the executable