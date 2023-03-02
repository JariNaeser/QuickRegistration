# QuickRegistration
A little embedded system that simplifies the registration of the present students in a lecture.

**Note**: This project was delevoped in italian

### About
In a lot of schools nowadays before the start of every lesson the teacher checks which students are present and which aren't. <br>
This operation is usually done through a sheet of paper and by hand. It is very repetitive and time consuming. <br>
Therefore I developed this little device that solves this problem through some simple sensors and a RFID card that every student owns.

### Components

...

### Raspberry pin configuration
In order to have a system that works with the given source file every pin has to strictly match the following table.

![RaspberryPi 3 pinout map](media/Raspberry_pinout.png) <br>
<small>**Image source**: [link](https://pi4j.com/1.2/pins/model-b-plus.html)</small>

| Component   | Component Pin | RaspberryPi pin (Board Layout) |
| ----------- | ------------- | ------------------------------ |
| LCD         | VCC (5V)      | 02              |
|             | SDA           | 03              |
|             | SCL           | 05              |
|             | GND           | 25              |
| Buzzer      | Signal (+)    | 37              |
|             | GND           | 39              |
| RFID Reader | GND           | 09              |
|             | VCC (3.3V)    | 17              |
|             | MOSI          | 19              |
|             | MISO          | 21              |
|             | RST           | 22              |
|             | SCK           | 23              |
|             | NSS           | 24              |
| RGB Led     | GND           | 06              |
|             | Green         | 07              |
|             | Red           | 11              |
|             | Blue          | 13              |


### Project structure

...

### How to setup

...