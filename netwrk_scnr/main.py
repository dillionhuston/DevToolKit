import portscn
import deviceinfo
#use this file to run what you need or you can just import into own project 

if __name__ == "__main__":
    host = str(input("enter host ip address"))
    deviceinfo.device_info(host=host, iface=None)


   