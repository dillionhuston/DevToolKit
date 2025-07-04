import jsonlines
import io
from scapy.all import ARP, Ether, srp, conf

def device_info(host, iface=None):
    try:
        print(f"avaliable ifaces{conf.ifaces}")
        print(f"Using interface: {iface if iface else conf.iface}")
        arp = ARP(pdst=host)
        broadcast = Ether (dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/arp
        answers, unanswered = srp(arp_request_broadcast, verbose=True, timeout=5, iface=iface)

        devices = []
        for element in answers:
            device_info = {"ip" : element[1].psrc, "mac": element[1].hwsrc}
            devices.append(device_info)

        if devices:    
            print("fiound devices")
            with jsonlines.open("devices.json", "w") as writer:
                for device in devices:
                    print(f"IP ADDR: {device['ip']}, MAC: {device['mac']}\n")  
                    writer.write(device)
        else:
            print("no devices")
            if unanswered:
                print("oackets were sent but dinit answer back ")
        return devices
    
    except Exception as e:
        print(f"erprr{e}")
        return []
    