## 1. Finding the VID and PID of your USB SSD

Disconnect the USB SSD. In a terminal window, run the command sudo dmesg -C.
Now, plug in the SSD and run dmesg with no parameters.
You should get output that looks like this:
Code: Select all

```
[ 4096.609817] usb 2-1: new SuperSpeed Gen 1 USB device number 4 using xhci_hcd
[ 4096.646369] usb 2-1: New USB device found, idVendor=2109, idProduct=0715, bcdDevice=a0.00
[ 4096.646385] usb 2-1: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[ 4096.646397] usb 2-1: Product: SABRENT
[ 4096.646409] usb 2-1: Manufacturer: SABRENT
[ 4096.646421] usb 2-1: SerialNumber: 000000123AD2
[ 4096.655154] scsi host0: uas
[ 4096.669178] scsi 0:0:0:0: Direct-Access              SABRENT          2210 PQ: 0 ANSI: 6
[ 4096.670993] sd 0:0:0:0: Attached scsi generic sg0 type 0
[ 4096.673710] sd 0:0:0:0: [sda] 234441648 512-byte logical blocks: (120 GB/112 GiB)
```

The idVendor and idProduct are the two hexadecimal numbers you need to take a note of.

## 1a. Multiple SSDs

If you have multiple USB SSD devices plugged into a single Pi 4, then for each device experiencing issues repeat Step 1 above and make a note of each idVendor and idProduct pair.

## 2. Add the quirks to /boot/cmdline.txt

Run a text editor as root - sudo nano /boot/cmdline.txt from the console or sudo leafpad /boot/cmdline.txt from the desktop.
At the start of the line of parameters, add the text usb-storage.quirks=aaaa:bbbb:u where aaaa is the idVendor for your device and bbbb is the idProduct. So, with the device above the string will be usb-storage.quirks=2109:0715:u.
cmdline.png
cmdline.png (21.45 KiB) Viewed 236625 times
For multiple devices with different VID:PID pairs, expand the parameter with a comma between each vid:pid:u triplet like this: usb-storage.quirks=0123:4567:u,2109:0715:u.

Save the file and exit the editor.

# 3. Reboot.

# 4. Check that it worked

# Resource 

- https://forums.raspberrypi.com/viewtopic.php?t=245931
