#!/usr/bin/env python3

from struct import unpack, pack
from tkinter import END

class PacketDefaultPayload():
    # class template tu use for a new object
    def __init__(self, payload) :
        self.payload = payload

    @staticmethod
    def parse(payload):
        return PacketDefaultPayload(payload)
    
    def encode(self):
        return self.payload
    
    def __str__(self) -> str:
        return f"Unknown payload: {self.payload.hex()}"

class PacketNewInventoryPayload():
    # class template tu use for a new object
    def __init__(self, name_len, name, qty) :
        self.name_len = name_len
        self.name = name
        self.quantity = qty

    @staticmethod
    def parse(payload):
        name_len = int.from_bytes(payload[:2], 'little')
        name = payload[2:2+name_len].decode()
        qty = int.from_bytes(payload[2+name_len:2+name_len+4],'little')
        return PacketNewInventoryPayload(name_len, name, qty)
    
    def encode(self):
        return self.name_len.to_bytes(2, 'little') + self.name.encode() + self.quantity.to_bytes(4,'little')
    
    def __str__(self) -> str:
        return f"New inventory: {self.name} {self.quantity}"

class PacketAttackStatePayload():
    # class template tu use for a new object
    def __init__(self, id, name_len, name, tag) :
        self.id = id
        self.name_len = name_len
        self.name = name
        self.tag = tag

    @staticmethod
    def parse(payload):
        id = int.from_bytes(payload[:4], 'little')
        name_len = int.from_bytes(payload[4:6], 'little')
        name = payload[6:6+name_len].decode()
        tag = int.from_bytes(payload[6+name_len:6+name_len+4], 'little')
        return PacketAttackStatePayload(id, name_len, name, tag)
    
    def encode(self):
        return self.id.to_bytes(4,'little') + self.name_len.to_bytes(2,'little') + self.name.encode() + self.tag.to_bytes(4,'little')
    
    def __str__(self) -> str:
        return f"Chg Attack state: {self.id} {self.name} {self.tag}"

class PacketRegistry:
    
    TYPE_TO_CLASS = {}

    @staticmethod
    def register(pkt_type, clazz):
        if pkt_type not in PacketRegistry.TYPE_TO_CLASS:
            PacketRegistry.TYPE_TO_CLASS[pkt_type] = clazz
    
    @staticmethod
    def get(pkt_type):
        if pkt_type in PacketRegistry.TYPE_TO_CLASS:
            return PacketRegistry.TYPE_TO_CLASS[pkt_type]
        else:
            return None

class packet_type:
    """
    Class decoraroe to register packet parser/forge classes
    """
    def __init__(self, pkt_type):
        self.pkt_type = pkt_type
    
    def __call__(self, clazz):
        PacketRegistry.register(self.pkt_type, clazz)
        return clazz

class PacketHeader():
    def __init__(self,pkt_hdr = None, type = 0):
        if pkt_hdr is not None:
            self.type = unpack(">H", pkt_hdr)[0]
        else:
            self.type = type

    @staticmethod
    def parse(pkt_hdr):
        type = unpack(">H", pkt_hdr)[0]
        return PacketHeader(type=type)
    
    def encode(self):
        return pack('>H', self.type)
    
    def __str__(self) -> str:
        return f"0x{self.type:x}"

class PacketItemPickPayload():
    # class template tu use for a new object
    def __init__(self, id) :
        self.id = id

    @staticmethod
    def parse(payload):
        return PacketItemPickPayload(int.from_bytes(payload[:4],'little'))
    
    def encode(self):
        return self.id.to_bytes(4,'little')
    
    def __str__(self) -> str:
        return f"Item pickup: {self.id}"

class PacketRemoveElmtPayload():
    # class template tu use for a new object
    def __init__(self, id) :
        self.id = id

    @staticmethod
    def parse(payload):
        return PacketRemoveElmtPayload(int.from_bytes(payload[:4],'little'))
    
    def encode(self):
        return self.id.to_bytes(4,'little')
    
    def __str__(self) -> str:
        return f"Remove element: {self.id}"

class PacketPlayerStatePayload():
    # class template tu use for a new object
    def __init__(self, id, name_len, name) :
        self.id = id
        self.name_len = name_len
        self.name = name

    @staticmethod
    def parse(payload):
        id = int.from_bytes(payload[:4],'little')
        name_len = int.from_bytes(payload[4:6],'little')
        name = payload[6:6+name_len].decode()
        return PacketPlayerStatePayload(id, name_len, name)
    
    def encode(self):
        return self.id.to_bytes(4,'little') + self.name_len.to_bytes(2, 'little') + self.name.encode() + b"\x00"
    
    def __str__(self) -> str:
        return f"Player change state:  {self.id} {self.name}"

class PacketNewElmtPayload():
    # class template tu use for a new object
    def __init__(self, id, unk1, name_len, name, X, Y, Z, unk2) :
        self.id = id
        self.unk1 = unk1
        self.name_len = name_len
        self.name = name
        self.X = X
        self.Y = Y
        self.Z = Z
        self.unk2 = unk2

    @staticmethod
    def parse(payload):
        id = int.from_bytes(payload[:4],'little')
        unk1 = payload[4:9]
        name_len = int.from_bytes(payload[9:9+2],'little')
        name = payload[11:11+name_len].decode()
        X, Y, Z = unpack("fff",payload[11+name_len:11+name_len+12])
        unk2 = payload[11+name_len+12:11+name_len+12+10]
        return PacketNewElmtPayload(id, unk1, name_len, name, X, Y, Z, unk2)
    
    def encode(self):
        ret = self.id.to_bytes(4,'little') + self.unk1
        ret += self.name_len.to_bytes(2,'little') + self.name.encode()
        ret += pack("fff", self.X, self.Y, self.Z)
        ret += self.unk2
        return ret
    
    def __str__(self) -> str:
        return f"New element: {self.id}:{self.name} {self.X} / {self.Y} / {self.Z} {self.unk2.hex()}"

class PacketFastTravelPayload():
    # class template tu use for a new object
    def __init__(self, src_name_len,src_name,dst_name_len,dst_name) :
        self.src_name_len: int = src_name_len
        self.src_name = src_name
        self.dst_name_len: int = dst_name_len
        self.dst_name = dst_name

    @staticmethod
    def parse(payload):
        src_name_len = int.from_bytes(payload[:2], 'little')
        src_name = payload[2:2+src_name_len].decode()
        dst_name_len = int.from_bytes(payload[2+src_name_len:2+src_name_len+2], 'little')
        dst_name = payload[2+src_name_len+2:2+src_name_len+2+dst_name_len].decode()
        return PacketFastTravelPayload(src_name_len,src_name,dst_name_len,dst_name)
    
    def encode(self):
        return self.src_name_len.to_bytes(2,'little') + self.src_name.encode() + self.dst_name_len.to_bytes(2,'little') + self.dst_name.encode()
    
    def __str__(self) -> str:
        return f"Fast Travel: {self.src_name} -> {self.dst_name}"

class PacketPositionPayload():
    '''
    Payload of Position type
    '''
    POSITION_SIZE = 20
    def __init__(self, X, Y, Z, look, unk, key):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.look = look
        self.unk = unk
        self.key = key

    @staticmethod
    def parse(payload):
        X, Y, Z, look, unk, key = unpack("fffIHH",payload[:PacketPositionPayload.POSITION_SIZE])
        return PacketPositionPayload(X, Y, Z, look, unk, key)
    
    def encode(self):
        return pack("fffIHH", self.X, self.Y, self.Z, self.look, self.unk, self.key)
    
    def __str__(self) -> str:
        return f"Position packet: {self.X} / {self.Y} / {self.Z} / {self.look}"


class PacketEnemyPosPayload():
    '''
    Payload of Position type of an Enemy
    '''
    def __init__(self, id, X, Y, Z, payload):
        self.id = id
        self.X = X
        self.Y = Y
        self.Z = Z
        self.payload = payload

    @staticmethod
    def parse(payload):
        id, X, Y, Z= unpack("Ifff",payload[:16])
        return PacketEnemyPosPayload(id, X, Y, Z, payload[16:])
    
    def encode(self):
        return pack("Ifff", self.id, self.X, self.Y, self.Z) + self.payload

   
    def __str__(self) -> str:
        return f"EnemyPos: ID:{self.id} {self.X} / {self.Y} / {self.Z} {self.payload[:10].hex()} ..."

class PacketReloadPayload():
    '''
    Payload of Reload of weapon type
    '''
    def __init__(self) :
        self.payload = b''

    @staticmethod
    def parse(payload):
        return PacketReloadPayload()
    
    def encode(self):
        return self.payload
    
    def __str__(self) -> str:
        return f"Reload"

class PacketBeaconPayload():
    '''
    Payload of Beacon type: check the connectivity
    '''
    def __init__(self, payload) :
        self.payload = payload

    @staticmethod
    def parse(payload):
        return PacketBeaconPayload(payload[:35])
    
    def encode(self):
        return self.payload
    
    def __str__(self) -> str:
        return f"Beacon: {self.payload.hex()}"

class PacketShootPayload():
    '''
    Payload of Shoot type from the player
    '''
    def __init__(self, name_size, name, payload) :
        self.payload = payload 
        self.name_size = name_size
        self.name = name

    @staticmethod
    def parse(payload):
        name_size = int.from_bytes(payload[:2], 'little')
        name = ''.join(chr(x) for x in payload[2:2+name_size])
        other = payload[2+name_size:2+name_size+12]
        return PacketShootPayload(name_size,name,other)
    
    def encode(self):
        return self.name_size.to_bytes(2, "little") + self.name.encode() + self.payload
    
    def __str__(self) -> str:
        return f"Shoot Arme:{self.name} Data:{self.payload.hex()}"

class ChangeToolPayload():
    '''
    Payload of Tool in hand of the user type
    '''
    def __init__(self, nb) :
        self.nb = nb

    @staticmethod
    def parse(payload):
        return ChangeToolPayload((payload[0]+1)%10)
    
    def encode(self):
        return self.nb.to_bytes(1,'big')
    
    def __str__(self) -> str:
        return f"Change Tool: {self.nb}"

class JumpPacketPayload():
    '''Jump packet payload'''
    def __init__(self, action) :
        self.action = action

    @staticmethod
    def parse(payload):
        if payload[0] == 1:
            return JumpPacketPayload("Up")
        else:
            return JumpPacketPayload("Down")
    
    def encode(self):
        if self.action == "Up":
            return b'\x01'
        else:
            return b'\x00'
    
    def __str__(self) -> str:
        return f"Jump: {self.action}"


class PacketBurstPayload():
    '''Burst packet to inform of the start and end of a burst'''
    def __init__(self, action) :
        self.action = action

    @staticmethod
    def parse(payload):
        action = payload[0]
        return PacketBurstPayload(action)
    
    def encode(self):
        return self.action.to_bytes(1, "little")
    
    def __str__(self) -> str:
        return f"Burst : {self.action}"


class PacketShootServerPayload():
    '''Shoot packet from the server payload'''
    def __init__(self, payload) :
        self.payload = payload

    @staticmethod
    def parse(payload):
        return PacketShootServerPayload(payload)
    
    def encode(self):
        return self.payload
    
    def __str__(self) -> str:
        return f"ShootServer: {self.payload.hex()}"


class PacketHPmodifPayload():
    '''Health Point packet'''
    def __init__(self, payload) :
        self.payload = payload

    @staticmethod
    def parse(payload):
        return PacketHPmodifPayload(payload)
    
    def encode(self):
        return self.payload
    
    def __str__(self) -> str:
        return f"HP modification: {self.payload.hex()}"


class PacketSellPayload():
    '''Sell on object packet'''
    def __init__(self, id, lenght_name, name, quantity) :
        self.id = id
        self.lenght_name = lenght_name
        self.name = name
        self.quantity = quantity

    @staticmethod
    def parse(payload):
        id = int.from_bytes(payload[0:4], 'little')
        lenght_name = int.from_bytes(payload[4:6], 'little')
        name = payload[6:lenght_name + 6].decode()
        quantity = int.from_bytes(payload[lenght_name + 6: lenght_name + 10], 'little')

        
        return PacketSellPayload(id, lenght_name, name, quantity)
    
    def encode(self):
        return self.id.to_bytes(4, "little") + self.lenght_name.to_bytes(2, "little") + self.name.encode() + self.quantity.to_bytes(4, "little")
    
    def __str__(self) -> str:
        return f"Sell: id {self.id} {self.name} {self.quantity}"

class PacketXchangePayload():
    ''' Exchange packet after buying or selling an object'''
    def __init__(self, lenght_name, name, quantity, data, lenghtxname, xname, coins) :
        self.lenght_name = lenght_name
        self.name = name
        self.quantity = quantity
        self.data = data
        self.lenghtxname = lenghtxname
        self.xname = xname
        self.coins = coins


    @staticmethod
    def parse(payload):
        lenght_name = int.from_bytes(payload[0:2], "little")
        name = payload[2:lenght_name + 2].decode()
        quantity = int.from_bytes(payload[lenght_name + 2: lenght_name + 6], 'little')
        data = payload[lenght_name + 6: lenght_name + 8]
        lenghtxname = int.from_bytes(payload[lenght_name + 8: lenght_name + 10], 'little')
        xname = payload[lenght_name + 10:lenghtxname + lenght_name + 10].decode()
        coins = int.from_bytes(payload[lenghtxname + lenght_name + 10: lenghtxname + lenght_name + 16], 'little')
        return PacketXchangePayload(lenght_name, name, quantity, data, lenghtxname, xname, coins)
    
    def encode(self):
        return self.lenght_name.to_bytes(2, "little") + self.name.encode() + self.quantity.to_bytes(4, "little") + self.data + self.lenghtxname.to_bytes(2, "little") + self.xname.encode() + self.coins.to_bytes(6, "little")
    
    def __str__(self) -> str:
        return f"Xchange: {self.name} {self.quantity} {self.xname} {self.coins}"

class Packet:
    HEADER_SIZE = 2

    def __init__(self, header, payload):
        self.header = header
        self.payload = payload


    @staticmethod
    def parse( packet):
        header = PacketHeader(packet[:Packet.HEADER_SIZE])
        pkt_clazz = PacketRegistry.get(header.type)
        if pkt_clazz is None:
            return Packet(header, PacketDefaultPayload.parse(packet[Packet.HEADER_SIZE:]))
        else:
            return pkt_clazz.parse(packet)

    def encode(self) -> bytes:
        return self.header.encode() + self.payload.encode()

    def __str__(self):
        return f"{self.header} {self.payload}"


# Decorators:

@packet_type(0x6d6b)
class NewElmtPacket(Packet):
    """New element"""
    TYPE = 0x6d6b

    @staticmethod
    def parse(packet):
        header = PacketHeader.parse(packet[:Packet.HEADER_SIZE])
        payload = PacketNewElmtPayload.parse(packet[Packet.HEADER_SIZE:])
        return NewElmtPacket(header, payload)


@packet_type(0x6d76)
class PositionPacket(Packet):
    TYPE = 0x6d76

    @staticmethod
    def parse(packet):
        header = PacketHeader.parse(packet[:Packet.HEADER_SIZE])
        payload = PacketPositionPayload.parse(packet[Packet.HEADER_SIZE:])
        return PositionPacket(header, payload)

@packet_type(0x7073)
class EnemyPosPacket(Packet):
    TYPE = 0x7073

    @staticmethod
    def parse(packet):
        header = PacketHeader.parse(packet[:Packet.HEADER_SIZE])
        payload = PacketEnemyPosPayload.parse(packet[Packet.HEADER_SIZE:])
        return EnemyPosPacket(header, payload)

@packet_type(0x6674)
class FastTravelPacket(Packet):
    TYPE = 0x6674

    @staticmethod
    def parse(packet):
        header = PacketHeader.parse(packet[:Packet.HEADER_SIZE])
        payload = PacketFastTravelPayload.parse(packet[Packet.HEADER_SIZE:])
        return FastTravelPacket(header, payload)

@packet_type(0x1703)
class BeaconPacket(Packet):
    TYPE = 0x1703 

    @staticmethod
    def parse(packet):
        header = PacketHeader.parse(packet[:Packet.HEADER_SIZE])
        payload = PacketBeaconPayload.parse(packet[Packet.HEADER_SIZE:])
        return BeaconPacket(header, payload)

@packet_type(0x6a70)
class JumpPacket(Packet):
    TYPE = 0x6a70

    @staticmethod
    def parse(packet):
        header = PacketHeader.parse(packet[:Packet.HEADER_SIZE])
        payload = JumpPacketPayload.parse(packet[Packet.HEADER_SIZE:])
        return JumpPacket(header, payload)

@packet_type(0x733D)
class ChangeTool(Packet):
    TYPE = 0x733D

    @staticmethod
    def parse(packet):
        header = PacketHeader.parse(packet[:Packet.HEADER_SIZE])
        payload = ChangeToolPayload.parse(packet[Packet.HEADER_SIZE:])
        return ChangeTool(header, payload)

@packet_type(0x726c)
class ReloadPacket(Packet):
    TYPE = 0x726c

    @staticmethod
    def parse(packet):
        header = PacketHeader.parse(packet[:Packet.HEADER_SIZE])
        payload = PacketReloadPayload.parse(packet[Packet.HEADER_SIZE:])
        return ReloadPacket(header, payload)

@packet_type(0x2a69)
class ShootPacket(Packet):
    TYPE = 0x2a69

    @staticmethod
    def parse(packet):
        header = PacketHeader.parse(packet[:Packet.HEADER_SIZE])
        payload = PacketShootPayload.parse(packet[Packet.HEADER_SIZE:])
        return ShootPacket(header, payload)


@packet_type(0x6672)
class BurstPacket(Packet):
    TYPE = 0x6672

    @staticmethod
    def parse(packet):
        header = PacketHeader.parse(packet[:Packet.HEADER_SIZE])
        payload = PacketBurstPayload.parse(packet[Packet.HEADER_SIZE:])
        return BurstPacket(header, payload)


@packet_type(0x6c61)
class PacketShootServer(Packet):
    TYPE = 0x6c61

    @staticmethod
    def parse(packet):
        header = PacketHeader.parse(packet[:Packet.HEADER_SIZE])
        payload = PacketShootServerPayload.parse(packet[Packet.HEADER_SIZE:])
        return PacketShootServer(header, payload)

@packet_type(0x2b2b)
class HPmodifPacket(Packet):
    TYPE = 0x2b2b

    @staticmethod
    def parse(packet):
        header = PacketHeader.parse(packet[:Packet.HEADER_SIZE])
        payload = PacketHPmodifPayload.parse(packet[Packet.HEADER_SIZE:])
        return HPmodifPacket(header, payload)

@packet_type(0x2473)
class SellPacket(Packet):
    TYPE = 0x2473

    @staticmethod
    def parse(packet):
        header = PacketHeader.parse(packet[:Packet.HEADER_SIZE])
        payload = PacketSellPayload.parse(packet[Packet.HEADER_SIZE:])
        return SellPacket(header, payload)

@packet_type(0x726d)
class XchangePacket(Packet):
    TYPE = 0x726d

    @staticmethod
    def parse(packet):
        header = PacketHeader.parse(packet[:Packet.HEADER_SIZE])
        payload = PacketXchangePayload.parse(packet[Packet.HEADER_SIZE:])
        return XchangePacket(header, payload)

@packet_type(0x7374)
class PlayerStatePacket(Packet):
    TYPE = 0x7374

    @staticmethod
    def parse(packet):
        header = PacketHeader.parse(packet[:Packet.HEADER_SIZE])
        payload = PacketPlayerStatePayload.parse(packet[Packet.HEADER_SIZE:])
        return PlayerStatePacket(header, payload)

@packet_type(0x7472)
class AttackStatePacket(Packet):
    TYPE = 0x7472

    @staticmethod
    def parse(packet):
        header = PacketHeader.parse(packet[:Packet.HEADER_SIZE])
        payload = PacketAttackStatePayload.parse(packet[Packet.HEADER_SIZE:])
        return AttackStatePacket(header, payload)

@packet_type(0X6565)
class ItemPickPacket(Packet):
    TYPE = 0X6565

    @staticmethod
    def parse(packet):
        header = PacketHeader.parse(packet[:Packet.HEADER_SIZE])
        payload = PacketItemPickPayload.parse(packet[Packet.HEADER_SIZE:])
        return ItemPickPacket(header, payload)

@packet_type(0x7878)
class RemoveElmtPacket(Packet):
    TYPE = 0x7878

    @staticmethod
    def parse(packet):
        header = PacketHeader.parse(packet[:Packet.HEADER_SIZE])
        payload = PacketRemoveElmtPayload.parse(packet[Packet.HEADER_SIZE:])
        return RemoveElmtPacket(header, payload)

@packet_type(0x6370)
class NewInventoryPacket(Packet):
    TYPE = 0x6370

    @staticmethod
    def parse(packet):
        header = PacketHeader.parse(packet[:Packet.HEADER_SIZE])
        payload = PacketNewInventoryPayload.parse(packet[Packet.HEADER_SIZE:])
        return RemoveElmtPacket(header, payload)

FILTERS_DICT = {
    'Show only unknown': 'pkt.header.type not in PacketRegistry.TYPE_TO_CLASS',
    'Whitelist': 'pkt.header.type in whitelist',
    'Blacklist': 'pkt.header.type not in blacklist'
}

blacklist = [PositionPacket.TYPE, BeaconPacket.TYPE, EnemyPosPacket.TYPE, JumpPacket.TYPE ]
whitelist = [ItemPickPacket.TYPE, NewInventoryPacket.TYPE]

FILTERS = list(FILTERS_DICT.keys())

def parse(data, conn_dir, window_text = None, filter_selected = None):
    """Parse packet"""
    if data == b'\x00\x00':
        return
    while len(data) != 0 :
        pkt = Packet.parse(data)
        data = data[len(pkt.encode()):]
        # if pkt.header.type not in PacketRegistry.TYPE_TO_CLASS:  # type == 'client' and  # unknown packets
        #   print(f"[{conn_dir}] {pkt}")
        
        if filter_selected is not None:
            condition = eval(FILTERS_DICT[filter_selected])
        else:
            condition = True

        if condition: # do not show blacklisted packets
            txt = f"[{conn_dir}] {pkt}\n"
            if window_text is not None:
                window_text.insert(END,txt)
                window_text.see(END)
            else:
                print(txt)

if __name__ == "__main__":
    pkt = Packet.parse(bytes.fromhex("7073a50d0000832c49c6f57402c776b832450000c472000068ff330000007073a60d00002aeac7c5556908c74bb12e450000d4530000b5ff8d0000007073a70d0000addffbc5d99622c727244e450000388a00000000000000007073a80d00004e6108c3099323c75e9a1a450000c03e00000500a00000007073a90d0000767a014547e20bc714aa1145000070d7000057007aff00006d76a20d00003b5fc2c6ea7de3c6241c2545e7fffffffcf17073a30d0000d6b0b1c6f1c2d5c67e382e4500003c800000c0fefeff00007073a40d000006c5cbc6984511c7a27e43450000e9b80000e4ff62ff00000000"))

    print(pkt)
