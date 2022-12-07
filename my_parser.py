
class Parser:
    def __init__(self, port, data):
        self.port = port
        self.cmd = data[:2]
        self.other = data[2:]
    
    def __str__(self):
        return f"{self.cmd.hex()} {self.other[:100].hex()}"

def parse(data, port, hdr):
    log = Parser(port, data)
    if hdr == 'client':
        print(f"{log}")