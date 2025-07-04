from scapy.all import ARP, Ether, srp

def device_info(host):

    arp = ARP(pdst=host)
    broadcast = Ether("ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp

    answers = srp(arp_request_broadcast, verbose = True)[0]

    devices = []
    for element in answers:
        device_info = {"ip" : element[1].psrc, "mac": element[1].hwsrc}
        devices.append(device_info)

        return devices
    