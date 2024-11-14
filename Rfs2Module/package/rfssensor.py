# Copyright (C) 2021 Intel Corporation 
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information

from package.sensor import *
from package.sensorcontroller import *

class RfsSensor(SensorController):
    def __init__(self,name='rfsSensors', real=False, offset=0x0) -> None:
        self.name = name
        self.modules = {
            'lux'           : Sensor('lux',             'float', real,        offset+0x4*2),
            'humidity'      : Sensor('humidity',        'float', real,        offset+0x4*3),
            'temperature'   : Sensor('temperature',     'float', real,        offset+0x4*4)
        }
        
        if(real) :
            logger.debug(" \n\
                    RfsSensors: \n\
                        Lux : \n\
                            Data : {} \n\
                        Humidity : \n\
                            Data : {} \n\
                        Temperature : \n\
                            Data : {} \n"
                .format(
                    hex(self.modules.get('lux').offset),
                    hex(self.modules.get('humidity').offset),
                    hex(self.modules.get('temperature').offset)
                )
            )