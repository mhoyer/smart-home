# Installing Raspbian Lite (headless)

## Get the image

Download the image as `.zip` from https://www.raspberrypi.org/downloads/raspbian/ and extract it

```bash
curl -L https://downloads.raspberrypi.org/raspbian_lite_latest -o raspbian_lite_latest.zip
unzip raspbian_lite_latest.zip
rm raspbian_lite_latest.zip
```

## Flash the SD Card

Insert SD card and check its device name and potentially mounted partitions with `lsblk -p`. We may have to unmount partitions that got mounted automatically by linux.

```bash
lsblk -p          # which device is our SD card? `/dev/sdc`?
umount /dev/sdc1
```

Now we are ready to copy the image to the card. **THIS WILL DESTROY ALL DATA!**

```bash
sudo dd bs=4M if=2019-09-26-raspbian-buster-lite.img of=/dev/sdc conv=fsync
```

## Pre-Initialize the SD Card

Now we can:

- enable SSH access for headless access
- give the `PI` a proper hostname (otherwise it will be `raspberrypi`)

```bash
lsblk -p
touch /media/$USER/boot/ssh               # an empty `ssh` file to enable SSH
sudo vi /media/$USER/rootfs/etc/hostname  # the hostname to make it unique
```

### Additional WIFI Support

If you do not want to connect the Raspberry Pi to the ethernet, you can also pre-configure your preferred WIFI network:

```bash
vi /media/$USER/boot/wpa_supplicant.conf
```

```ini
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=<Insert country code here>

network={
  ssid="<Name of your WiFi>"
  psk="<Password for your WiFi>"
}
```

See also: https://www.raspberrypi.org/documentation/configuration/wireless/headless.md

## First Boot

Unmount the `boot` and `rootfs` partitions:

```bash
umount /dev/sdc1
umount /dev/sdc2
```

Remove the SD card, plug it into the Raspberry Pi and boot it up with connected ethernet.

If you have DHCP installed you should find your Pi with the custom `hostname` set above:

```bash
ping raspberrypi      # alt. with the previously set hostname
ssh-copy-id pi@raspberrypi    # default password should be 'raspberry'
```

## Basic setup

```bash
passwd              # change password to something random
hostname <HOSTNAME> # change the hostname of your Pi
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
sudo apt-get install -y libffi-dev libssl-dev
sudo apt-get install -y python3 python3-pip
sudo apt-get remove python-configparser
sudo pip3 install docker-compose
```
