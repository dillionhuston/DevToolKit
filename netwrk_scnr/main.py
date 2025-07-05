import portscn
import deviceinfo
import vendor
#use this file to run what you need or you can just import into own project 

if __name__ == "__main__":
    answer = input("enter mac")
    vendor.GetVendor(mac=answer)
    


   