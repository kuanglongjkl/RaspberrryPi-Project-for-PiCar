from OledModule.OLED import OLED
import time

oled=OLED(16,20,0,0)
oled.setup()
oled.writeArea1('test')
oled.writeArea2('tesst')
oled.writeArea3('tesftg')
oled.writeArea4('testggg')
time.sleep(2)
oled.clearArea1()
time.sleep(2)
oled.clearArea2()
time.sleep(2)
oled.clearArea3()
time.sleep(2)
oled.clearArea4()
oled.writeArea1('hello')
time.sleep(2)
oled.clear()