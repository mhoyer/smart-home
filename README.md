# Installing Raspbian Lite (headless)

## Get the image

Download the image as `.zip` from https://www.raspberrypi.org/software/operating-systems/#raspberry-pi-os-32-bit and extract it

```bash
curl -L https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2020-12-04/2020-12-02-raspios-buster-armhf-lite.zip -o 2020-12-02-raspios-buster-armhf-lite.zip
unzip 2020-12-02-raspios-buster-armhf-lite.zip
rm 2020-12-02-raspios-buster-armhf-lite.zip
```

## Flash the SD Card

Insert SD card and check its device name and potentially mounted partitions with `lsblk -p`. We may have to unmount partitions that got mounted automatically by linux.

```bash
lsblk -p          # which device is our SD card? `/dev/sdc`?
umount /media/$USERNAME/*
```

Now we are ready to copy the image to the card. **THIS WILL DESTROY ALL DATA!**

```bash
sudo dd bs=4M if=2020-12-02-raspios-buster-armhf-lite.img of=/dev/sdc conv=fsync status=progress
```

## Pre-Initialize the SD Card

Now we can:

- enable SSH access for headless access
- give the `PI` a proper hostname (otherwise it will be `raspberrypi`)

```bash
lsblk -p
touch /media/$USER/boot/ssh                 # an empty `ssh` file to enable SSH
sudo nano /media/$USER/rootfs/etc/hostname  # the hostname to make it unique
```

### Additional WIFI Support

If you do not want to connect the Raspberry Pi to the ethernet, you can also pre-configure your preferred WIFI network:

```bash
nano /media/$USER/boot/wpa_supplicant.conf
```

```ini
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=DE

network={
  ssid="<Name of your WiFi>"
  psk="<Password for your WiFi>"
}
```

See also: https://www.raspberrypi.org/documentation/configuration/wireless/headless.md

## First Boot

Unmount the `boot` and `rootfs` partitions:

```bash
umount /media/$USER/*
```

Remove the SD card, plug it into the Raspberry Pi and boot it up with connected ethernet.

If you have DHCP installed you should find your Pi with the custom `hostname` set above:

```bash
ping <HOSTNAME>              # alt. with the previously set hostname
ssh-copy-id pi@<HOSTNAME>    # default password should be 'raspberry'
```

## Boot from SSD

See: https://www.tomshardware.com/how-to/boot-raspberry-pi-4-usb

Change boot options:

```bash
sudo raspi-config
# 6 Advanced Options
#   A6 Boot Order
#     -> USB Boot
#   A7 Bootloader Version
#     E1 Latest
#       -> **No** (Do NOT reset to defaults)
# Finish
#  -> **No** reboot

sudo dd if=/dev/mmcblk0 of=/dev/sda bs=1M conv=fsync status=progress
sudo shutdown now
```

Now power off the Pi, remove the SD card and turn it on again.

## Basic setup

```bash
passwd              # change password to something random
sudo raspi-config
# Advanced -> Expand disk
# Locale Settings ->
#  -> de_DE.UTF-8
#  -> en_US.UTF-8

sudo nano /boot/config.txt
# disable wifi
# disable bluethoot
```

### Enable `cgroup_enable=memory`

This is for docker as it shows up in logs as an error. See: https://www.gerbenvanadrichem.com/infrastructure/docker-on-raspbian-cgroup-not-supported-on-this-system/

```bash
sudo echo "cgroup_enable=memory" >> /boot/cmdline.txt
```

### Enable quirks mode for second SSD

See: [SSD-ISSUE](./SSD-ISSUE.md)

### Update packages and firmware

```bash
sudo sh -c '
apt update
apt full-upgrade -y -o Acquire::ForceIPv4=true
echo "y" | rpi-update

reboot now'
```

Update bootloader:

```bash
sudo rpi-eeprom-update -d -a
sudo reboot now
```

## Install Docker and `docker-compose`

See: https://dev.to/rohansawant/installing-docker-and-docker-compose-on-the-raspberry-pi-in-5-simple-steps-3mgl

### Pre-requisits

```bash
sudo apt install apt-transport-https ca-certificates curl gnupg2 python-pip
```

### Docker

```bash
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker pi
```

### `docker-compose`

```bash
sudo apt-get install -y libffi-dev libssl-dev python3 python3-pip
sudo apt-get remove python-configparser
sudo pip3 install docker-compose
```
