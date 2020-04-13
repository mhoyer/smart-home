# Flashing and Connecting the WeBee CC2350+CC2591 Module to a Raspberry Pi 4

## Found Documentation About WeBee Z-0002 Module

It was a little bit tricky to find documentation about my ordered CC2350+CC2591 module. On [gudreview](http://www.gudreviews.com/transmitters-receivers-module/571899904/webee-ti-cc-cc-zigbee-wireless.html) I found a link to a [Baidu file share](http://pan.baidu.com/s/1i5IY2lJ) which required an account to access it. I fetched the docs and found my `Z-0002` module on one of the four PDF documents.

The CC2350+CC2591 from WeBee has two sockets which are described in the manual found above as so:

```
      GND |xo| P2_4
     P2_3 |oo| P2_2 (DC)          GND |xo| VCC
(DD) P2_1 |oo| P2_0       (RESET) RST |oo| VCC
     P1_7 |oo| P1_6        (SET) P0_0 |oo| P0_1
     P1_5 |oo| NC      (UART RX) P0_2 |oo| P0_3 (UART TX)
     P1_3 |oo| P1_2              P0_4 |oo| P0_5
       NC |oo| P1_0 (CONN)       P0_6 |oo| NC
```

## Flashing with the Pi 4 (w/o CC Debugger)

Similar to [LeMaRiva - Flashing a CC2531 dongle using a Raspberry Pi](https://lemariva.com/blog/2019/08/zigbee-flashing-cc2531-using-raspberry-pi-without-cc-debugger) the wiring of the Pi 4 to the CC2350+CC2591 (for flashing) should look like:

PI4              | CC2350+CC2591
--               | --
Pin `39` or `06` | `GND`
Pin `38`         | `DD` (P2_1)
Pin `36`         | `DC` (P2_2)
Pin `35`         | `RST` (RESET)
Pin `01`         | `VCC` (3.3v)

Remark: as the CC2350+CC2591 is not an USB device we also have to power up with the 3.3V `VCC` pins.

### Download `cc_flash`

Don't fear the repository name - the `flash_cc2531` also worked for me with my CC2530+CC2591.

```bash
sudo apt update
sudo apt install wiringpi git
git clone https://github.com/jmichault/flash_cc2531
cd flash_cc2531
```

If the wiring (for flashing) is correct, `cc_chipid` should response some value (not `0000` or `ffff`) for `ID`:

```bash
./cc_chipid
# ID = a524.
```

If `0000` or `ffff` is returned, something is wrong. Re-check your wiring.

### Do The Flashing

First we should grab the firmware image from [@Koenkk]()

```bash
wget https://github.com/Koenkk/Z-Stack-firmware/raw/master/coordinator/Z-Stack_Home_1.2/bin/default/CC2530_CC2591_DEFAULT_20190608.zip

unzip CC2530_CC2591_DEFAULT_20190608.zip
# Archive:  CC2530_CC2591_DEFAULT_20190608.zip
#   inflating: CC2530ZNP-Prod.hex
#   inflating: CC2530ZNP-Prod.bin
```

Erase the flash and write the image:

```bash
./cc_erase
#   ID = a524.
#   erase result = 00a6.

./cc_write CC2530ZNP-Prod.hex
#   ID = a524.
#   reading line 15490.
#   file loaded (15497 lines read).
# writing page 128/128.
# verifying page 128/128.
#  flash OK.
```

Now we can disconnect the wires.

## Connecting the CC2350+CC2591 to the Pi

### Enabling an Additional UART Port

We are going to connect the ZigBee controller using UART to our Pi 4. Therefore, we have to [activate an UART port](https://lb.raspberrypi.org/forums/viewtopic.php?t=244827) like so:

```bash
dtoverlay -a | grep uart
#  midi-uart0
#  midi-uart1
#  miniuart-bt
#  pi3-miniuart-bt
#  uart0
#  uart1
#  uart2
#  uart3
#  uart4
#  uart5
```

Let's pick `uart2` and find the GPIO pins to be used for wiring:

```bash
dtoverlay -h uart2
# Name:   uart2
# Info:   Enable uart 2 on GPIOs 0-3
# Usage:  dtoverlay=uart2,<param>
# Params: ctsrts   Enable CTS/RTS on GPIOs 2-3 (default off)
```

As we don't need flow control we can use this line in our `/boot/config`:

```ini
dtoverlay=uart2        # without flow control pins
# dtoverlay=uart3,ctsrts # with flow control pins
```

After a reboot we should then find the additional `/dev/ttyAMA1` device:

```bash
ls -la /dev/ttyAMA*
# crw-rw---- 1 root dialout 204, 64 Mar 29 08:05 /dev/ttyAMA0
# crw-rw---- 1 root dialout 204, 65 Mar 29 08:05 /dev/ttyAMA1
```

### Wiring of the Pi 4 to the CC2350+CC2591

According to ["How do I make serial work on the Raspberry Pi3 (or later model) => Raspberry Pi4 UART"](https://raspberrypi.stackexchange.com/a/107780) we have this UART pin usage:

```
        TXD RXD CTS RTS     Board Pins
uart0   14  15              8   10
uart1   14  15              8   10
uart2   0   1   2   3       27  28  (I2C)
uart3   4   5   6   7       7   29
uart4   8   9   10  11      24  23  (SPI0)
uart5   12  13  14  15      32  33  (gpio-fan)
```

Which results in this connection schema for `uart2`:

PI4              | CC2350+CC2591
--               | --
Pin `39` or `06` | `GND`
Pin `27` (TX)    | `RX` (P0_2)
Pin `28` (RX)    | `TX` (P0_3)
Pin `01`         | `VCC` (3.3v)

For [zigbee2mqtt](https://www.zigbee2mqtt.io/) we have to add this connection settings to the `configuration.yml`:

```yaml
serial:
  port: /dev/ttyAMA1
advanced:
  baudrate: 115200
  rtscts: false
```

## Resources

- [LeMaRiva - #Zigbee: Flashing a CC2531 dongle using a Raspberry Pi](https://lemariva.com/blog/2019/08/zigbee-flashing-cc2531-using-raspberry-pi-without-cc-debugger)
- [How to select and flash CC2530](http://ptvo.info/how-to-select-and-flash-cc2530-144/)
- [Connecting the CC2530](https://www.zigbee2mqtt.io/information/connecting_cc2530.html)
- [Pi Pinout](https://pinout.xyz/)
- [Pi-Forum: Pi-4 Activating additional UART ports](https://lb.raspberrypi.org/forums/viewtopic.php?t=244827)
