# ADS1118_driver
# Created at 2025-02-09 16:14:00

# author: Richard Heming
# Port to MicroPython Richard Heming & uniGPT & Copilot ;-)

# for instrument pag & scale = 2048 min !!
import machine
#from machine import Pin
import time
import struct

class ADS1118():
    # MicroPython SPI considerations
    # we transmit 16bit over MOSI
    config_command = bytearray(2)
    # commands = [bytearray(2), bytearray(2), bytearray(2), bytearray(2)]
    # commands = []
    cmd_cnt = 0  # command counter

    startSingleShot = True
    MUX_AIN0_AIN1 = '000'
    MUX_AIN0_AIN3 = '001'
    MUX_AIN1_AIN3 = '010'
    MUX_AIN2_AIN3 = '011'
    MUX_AIN0 = '100'
    MUX_AIN1 = '101'
    MUX_AIN2 = '110'
    MUX_AIN3 = '111'
    PGA_6_114V = '000'
    PGA_4_096V = '001'
    PGA_2_048V = '010'
    PGA_1_024V = '011'
    PGA_0_512V = '100'
    PGA_0_256V_A = '101'  # equivalent to PGA_0_256V
    PGA_0_256V_B = '110'  # equivalent to PGA_0_256V
    PGA_0_256V = '111'
    MODE_CONTINUOUS = '0'
    MODE_SINGLESHOT = '1'
    DATARATE_8_SPS = '000'
    DATARATE_16_SPS = '001'
    DATARATE_32_SPS = '010'
    DATARATE_64_SPS = '011'
    DATARATE_128_SPS = '100'
    DATARATE_250_SPS = '101'
    DATARATE_475_SPS = '110'
    DATARATE_860_SPS = '111'
    TS_MODE_ADC = '0'
    TS_MODE_TEMP = '1'

    # void place holders
    #PGA_TEMP = '010'  # Using PGA_2_048V for temperature sensor
    SCALE_6_114V = '000'
    SCALE_4_096V = '001'
    SCALE_2_048V = '010'
    SCALE_1_024V = '011'
    SCALE_0_512V = '100'
    SCALE_0_256V_A = '101'
    SCALE_0_256V_B = '110'
    SCALE_0_256V = '111'
    

    ADC_CONVERSION_FACTORS = {
        PGA_6_114V: 6.114 / 32767,
        PGA_4_096V: 4.096 / 32767,
        PGA_2_048V: 2.048 / 32767,
        PGA_1_024V: 1.024 / 32767,
        PGA_0_512V: 0.512 / 32767, #        
        PGA_0_256V_A: 0.256 / 32767,
        PGA_0_256V_B: 0.256 / 32767,
        PGA_0_256V: 0.256 / 32767
    }

    ADC_SCALING_FACTORS = {
        SCALE_6_114V: 6114,
        SCALE_4_096V: 4096,
        SCALE_2_048V: 2048, #        SCALE_TEMP: 2048  # 2.048V at 0°C
        SCALE_1_024V: 1024,
        SCALE_0_512V: 512,
        SCALE_0_256V_A: 256,
        SCALE_0_256V_B: 256,
        SCALE_0_256V: 256,
    }
    SCALE_TEMP = 2048 / 32767  # Using SCALE_2_048V for temperature sensor
    print("definitions done..")

    # def __init__(self, nss=D5, mux_arr=[MUX_AIN0]):
    def __init__(self, nss=5, mux_arr=[MUX_AIN0_AIN1]):
        # for spiDev we have CS0 = D5 and CS1 = D22...
        self.commands = []
        try:
            # es müssen exakt die selben Namen genommen werden!
            # change CLK from 5000 to 50.000!
            self.spi = machine.SPI(1, baudrate=50000, polarity=0, phase=1, bits=8, sck=machine.Pin(18),
                                  mosi=machine.Pin(23), miso=machine.Pin(19)) # D18, D19 und D23 !
            self.nss = machine.Pin(nss, machine.Pin.OUT) # "5" = D5 = SS
            self.nss.value(1)
            print("Spi Device at /CS", nss, "set..") # chip select/ slave select
            # self.print_res(self.handle) # FEHLER!!
        except Exception as e:
            print(e)
        print("ADS1118 driver 2025-04-03.")
        time.sleep_ms(100)  # unnütz!
        print(mux_arr)  # ok!
        try:
            for i in range(len(mux_arr)):
                print("mux", mux_arr[i])  # ok!
                # self.print_res(self.commands[i])

                # other, special ranges
                if mux_arr[i] == self.MUX_AIN2:  # unused now (was SAM)
                    print("AIN2:")
                    self.config_command = self._encodeCommand(mux=mux_arr[i],
                                                               pga=self.PGA_0_512V)  # ok!
                    self.print_res(self.config_command)  # ok!
                    # self.commands[i](self.config_command)
                    self.commands.append(self.config_command)
                if (mux_arr[i] == self.MUX_AIN3):  # Ga!!
                    print("AIN3:")
                # low range
                    self.config_command = self._encodeCommand(mux=mux_arr[i],
                                                               pga=self.PGA_0_512V)  # ok!
                    self.print_res(self.config_command)  # ok!
                    # self.commands[i](self.config_command)
                    self.commands.append(self.config_command)
                # high range
                    self.config_command = self._encodeCommand(mux=mux_arr[i],
                                                               pga=self.PGA_6_114V)  # ok!
                    self.print_res(self.config_command)  # ok!
                    # self.commands[i](self.config_command)
                    self.commands.append(self.config_command)
                else:
                    # default ranges with isoamp gain of 16.2x
                    self.config_command = self._encodeCommand(mux=mux_arr[i])  # ok!
                    self.print_res(self.config_command)  # ok!
                    # self.commands[i](self.config_command)
                    self.commands.append(self.config_command)
                    # print("mux", mux_arr[i])
            # print("summary:")
            # self.cmd_cnt = 0
            # for i in range(len(self.commands)):
            #     self.print_res(self.commands[i])
        except Exception as e:
            print(e)

    def _encodeCommand(self, startSingleShot=False, mux=MUX_AIN0_AIN1, pga=PGA_2_048V, mode=MODE_CONTINUOUS,
                        datarate=DATARATE_250_SPS, tsMode=TS_MODE_ADC, pullupEnable=True, nop=False):
        if startSingleShot:
            outputS = '1'
        else:
            outputS = "0"
        outputS += str(mux)
        outputS += str(pga)
        outputS += str(mode)
        outputS += str(datarate)
        outputS += str(tsMode)
        if pullupEnable:
            outputS += '1'
        else:
            outputS += "0"
        if nop:
            outputS += "00"
        else:
            outputS += "01"
        # make the end
        outputS += "1"
        # debug
        # print("CONFIG:", outputS)
        # 16bit mode to make it short ;-)
        return bytearray([int(outputS[:8], 2), int(outputS[8:], 2)])
        # 32bit mode...
        # return bytearray([int(outputS[:8], 2), int(outputS[8:], 2), int(outputS[:8], 2), int(outputS[8:], 2), ])

    # def readData(self, mux=MUX_AIN0_AIN1, tsMode=TS_MODE_ADC, pga=PGA_2_048V):
    def readData(self, mux=0, tsMode=TS_MODE_ADC, pga=PGA_2_048V, scale=SCALE_2_048V):
        try:
            # debug
            outArr = bytearray(2)
            # self.print_res(self.config_command)
            # try to write_readinto 16bits...
            self.nss.value(0) # SELECT
            time.sleep_ms(1)  # Short delay before SPI transfer
            self.spi.write_readinto(self.commands[mux], outArr)
            self.nss.value(1) # UNSELECT
            # print("spi write_readinto ok..")
        except Exception as e:
            print("spi write error...!", e)
        # make the 16bit word
        #print("Received data:", outArr)
        out = outArr[0]* 256 + outArr[1]
        # debug
        # self.print_res(outArr)
        # print("factor:", self.ADC_CONVERSION_FACTORS[pga])
        if out >= 0x8000:
            out -= 0x10000
        if tsMode == self.TS_MODE_ADC:
            # preparation for the 16-bit ble stacking...as tupel
            return (out * self.ADC_CONVERSION_FACTORS[pga], out, self.ADC_SCALING_FACTORS[scale])
        else:
            # Temp Mode
            # make command and measure
            try:
                # first measurement measures perhaps a voltage...
                voidVal = bytearray(2)
                outTemp = bytearray(2)
                time.sleep_ms(50)  # this pause is essential!
                self.nss.value(0)
                self.spi.write_readinto(self._encodeCommand(tsMode=self.TS_MODE_TEMP), voidVal)
                self.nss.value(1)
                #print("voltage:", self.print_res(outTemp))
                time.sleep_ms(50)  # this pause is essential!
                # now we measure safely the chip temperatures...and prepare for ADC...
                self.nss.value(0)
                self.spi.write_readinto(self._encodeCommand(tsMode=self.TS_MODE_TEMP), outTemp)
                self.nss.value(1)
                #print("chip temperature", self.print_res(outTemp))
                # now, prepare for ADC
                # empty the data register..!
                # sleep(200)
                # voidVal = self.spi.write_readinto(self.commands[mux])
                # self.spi.unselect()
                time.sleep_ms(50)  # this pause is mandatory!
                self.nss.value(0)
                self.spi.write_readinto(self.commands[mux], voidVal )
                self.nss.value(1)
                # sleep(200) # this pause is mandatory!
                # self.spi.select()
                # voidVal = self.spi.write_readinto(self._encodeCommand(tsMode=self.TS_MODE_ADC))
                # self.spi.unselect()
            except Exception as e:
                print("spi write error...!", e)
            temp = outTemp[0]* 256 + outTemp[1]
            #print("temp:", temp)
            # easy formula only for positive temperatures :-)
            # preparation for the 16-bit ble stacking...as tupel
            return ((temp >> 2) * self.SCALE_TEMP, temp,
                     self.ADC_SCALING_FACTORS[scale])

    # Helper function to print bytearrays
    def print_res(self, b):
        print("command[", self.cmd_cnt, "] bytearray is: ", end="")
        self.cmd_cnt += 1
        for hd in b:
            print(f'{hd:02X}', end="") # conversion from hexadecimal to decimal with leading zero ;-)
        print("")


# not possible in Zerynth and MicroPython :(
if __name__ == "__main__":
    print("local testing with additional definitions - he 2025_04_03")
    print("test me: exec(open('ads1118.py').read())")
    from machine import Pin
    # defs
    # Defintions for the hardware:
    # copy from the ADS1118_driver
    TS_MODE_ADC      = '0'
    TS_MODE_TEMP     = '1'
    # ADC@D5 CH9-12 (diff 9,10 and single-ended 11,12)
    # 2 differential inputs
    MUX_AIN0_AIN1    = '000' # PIN1-2
    #MUX_AIN2_AIN3    = '011' # PIN3-4
    MUX_AIN2         = '110' # PIN3
    MUX_AIN3         = '111' # PIN4
    # ADC@D22 CH0-3 and CH4-8
    # 2 differential inputs
    MUX_AIN0_AIN1    = '000' # PIN1-2
    MUX_AIN2_AIN3    = '011' # PIN3-4

    PGA_6_114V       = '000'
    PGA_4_096V       = '001'
    PGA_2_048V       = '010'
    PGA_1_024V       = '011'
    PGA_0_512V       = '100'
    # Scale
    SCALE_6_114V    = '000'
    SCALE_4_096V    = '001'
    SCALE_2_048V    = '010'
    SCALE_1_024V    = '011'  
    SCALE_0_512V    = '100' 

    #not used...
    MUX_AIN0         = '100'
    MUX_AIN1         = '101'
    MUX_AIN2         = '110'
    MUX_AIN3         = '111'

    # for MicroPython CS0 und CS1 definitions
    D5 = 5
    D22 = 22


    # pin defs for the current measurement v1.0 board
    # INS and OUTS
    # Init LED
    LED0 = Pin(2, Pin.OUT)
    LED0.value(0)

    # CH0-3
    # pinMode(A1,OUTPUT) #A..ok
    # pinMode(A0,OUTPUT) #B..ok
    A1 = Pin(33, Pin.OUT) #A..ok - "D33"
    A0 = Pin(32, Pin.OUT) #B..ok - "D32"
    # CH4-8
    # pinMode(D12,OUTPUT) #A..ok
    # pinMode(D13,OUTPUT) #B..ok
    D12 = Pin(12, Pin.OUT) #A..ok - "D12"
    D13 = Pin(13, Pin.OUT) #B..ok - "D13"
    #CH9-12
    # pinMode(A2,INPUT) #A..only input!
    # pinMode(A3,INPUT) #B..Only input!
    A2 = Pin(34, Pin.IN) #A..only input! - "D34"
    A3 = Pin(35, Pin.IN) #B..Only input! - "D35"
    # pinMode(D14,OUTPUT) #A
    # pinMode(D27,OUTPUT) #B
    D14 = Pin(14, Pin.OUT) #A..ok - "D14"
    D27 = Pin(27, Pin.OUT) #B..ok - "D27"    
    
#     try:
#         adc = ads1118.ADS1118(5)
#     except Exception as e:
#         print(e)
#     print("abs. voltage:", adc.readData())
    
    #ADS1118 stufff#####################################################################
    try:
        # invoke the driver
        #adc1 = ads1118.ADS1118(D5, [MUX_AIN0_AIN3,MUX_AIN1_AIN3,MUX_AIN2_AIN3])
        #adc1 = ads1118.ADS1118(D5, [MUX_AIN0_AIN1,MUX_AIN2_AIN3])
        #adc1 = ads1118.ADS1118(D5, [MUX_AIN0, MUX_AIN1,MUX_AIN2,MUX_AIN3])
        adc1 = ads1118.ADS1118(D5, [MUX_AIN0_AIN1,MUX_AIN2,MUX_AIN3]) # diff and single-ended
        # ranges for pascal
            #bytearray[0] is:04AB...diff, PGA_2_048V, default
            #bytearray[1] is:68AB...se, PGA_0_512V..(MUX_AIN2)
            #bytearray[2] is:64AB...se, PGA_2_048V, default..(MUX_AIN2)
            #bytearray[3] is:78AB...se..Ga, PGA_0_512V..(MUX_AIN3)
            #bytearray[4] is:70AB...se..Ga, PGA_6_144V, ..(MUX_AIN3)
        #adc2 = ads1118.ADS1118(D22, [MUX_AIN0_AIN1,MUX_AIN2_AIN3])
        adc2 = ads1118.ADS1118(D22, [MUX_AIN0_AIN1,MUX_AIN2_AIN3]) # all differential
        #print("adc2", type(adc2))
    except Exception as e:
        print(e)     
