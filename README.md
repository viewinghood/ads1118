# 🎛️ ADS1118 MicroPython Driver

<div align="center">

[![MicroPython](https://img.shields.io/badge/MicroPython-2B2B2B?style=for-the-badge&logo=python&logoColor=white)](https://micropython.org)
[![ESP32](https://img.shields.io/badge/ESP32-E7352C?style=for-the-badge&logo=espressif&logoColor=white)](https://www.espressif.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

## 📝 Description

A pure MicroPython driver for the Texas Instruments ADS1118 16-bit Analog-to-Digital Converter (ADC) with integrated temperature sensor. This driver is specifically designed for the ESP32 DEV KIT V1 board.

## ✨ Features

- 🎯 16-bit ADC resolution
- 🌡️ Integrated temperature sensor
- 🔄 Configurable sampling rates (8SPS to 860SPS)
- ⚡ Multiple programmable gain amplifier (PGA) settings
- 🔌 SPI interface support
- 📊 Differential and single-ended input modes
- 🔧 Easy-to-use Python interface

## 🛠️ Hardware Requirements

- ESP32 DEV KIT V1
- ADS1118 ADC
- Connection wires

## 🔌 Pin Configuration

| ESP32 Pin | ADS1118 Pin | Description |
|-----------|-------------|-------------|
| D5        | CS0         | Chip Select |
| D22       | CS1         | Chip Select |
| D18       | SCK         | SPI Clock   |
| D19       | MISO        | SPI MISO    |
| D23       | MOSI        | SPI MOSI    |
| 3.3V      | VDD         | Power       |
| GND       | GND         | Ground      |

## 📦 Installation

1. Copy the `ads1118.py` file to your ESP32 device
2. Import the driver in your MicroPython code:

```python
from ads1118 import ADS1118
```

## 💻 Usage Examples

### Basic Voltage Reading
```python
from ads1118 import ADS1118

# Initialize the ADC with default settings
# corresponds to D5 = SPI-CS0 on ESP32
adc = ADS1118()  # inputs= IN0 & IN1 (differentail)

# Read voltage from AIN0_AIN1 
voltage, raw, scale = adc.readData()
# gives a tuple of voltage in V, raw value and the input-scale 
print(f"Voltage: {voltage:.3f}V, Raw: {raw}, Scale: {scale}") 

# A more detailed definition could make the 4 inputs to 2 pair full differential
# All "commands" for the operation (e.g. high-speed sampling, gain settings)
# must be done in this object. 
adc = ads1118.ADS1118(D22, [MUX_AIN0_AIN1,MUX_AIN2_AIN3])

# Read voltage from first pair AIN0_AIN1
voltage, raw, scale = adc.readData(mux=ADS1118.MUX_AIN0)
# Read voltage from second pair MUX_AIN2_AIN3
voltage2, raw2, scale = adc.readData(mux=ADS1118.MUX_AIN0)
print(f"Voltage: {voltage:.3f}V, Raw: {raw}, Scale: {scale}")
```

### Temperature Reading
```python
from ads1118 import ADS1118

# Initialize the ADC
adc = ADS1118(D5)

# Read temperature (you need to overwrite the default tsMode)
temp, raw, scale = adc.readData(tsMode=ADS1118.TS_MODE_TEMP)
print(f"Temperature: {temp:.1f}°C")
```

## 📊 Complete Example with Error Handling
```python
from ads1118 import ADS1118
import time

def read_sensors(adc):
    try:
        # Read temperature
        temp, raw_temp, scale = adc.readData(tsMode=ADS1118.TS_MODE_TEMP)
        print(f"Temperature: {temp:.1f}°C")
        
        # Read differential voltage
        diff_voltage, raw_diff, scale = adc.readData(mux=0, pga=PGA_0_512V, scale=SCALE_0_512V)
        print(f"Differential Voltage 1-2: {diff_voltage:.3f}V")
        
        # Read voltage on In2
        voltage2, raw_voltage2, scale2 = adc.readData(mux=1, pga=PGA_4_096V, scale=SCALE_4_096V)
        print(f"Voltage 2: {voltage2:.3f}V")

        # Read voltage on In3
        voltage3, raw_voltage3, scale3 = adc.readData(mux=2, pga=PGA_4_096V, scale=SCALE_4_096V)
        print(f"Voltage 3: {voltage3:.3f}V")        
        
    except Exception as e:
        print(f"Error reading sensors: {e}")
        # Reset the ADC if needed
        machine.reset()

# Initialize the ADC
adc = ads1118.ADS1118(D5, [MUX_AIN0_AIN1,MUX_AIN2,MUX_AIN3]) # diff and single-ended

# Main loop
while True:
    read_sensors(adc)
    time.sleep(1)  # Read every second

## 📄 License

MIT License

Copyright (c) 2025 Richard Heming

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For any questions or suggestions, please open an issue in the repository.