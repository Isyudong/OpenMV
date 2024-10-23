import sensor, image, time
from pyb import Pin

Sensing = Pin('P0',Pin.IN)
Kv_switch = Pin('P1',Pin.OUT_OD)
i = 0

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()


while(True):
    clock.tick()
    img = sensor.snapshot().lens_corr(1.8)
    for c in img.find_circles(roi=(75,1,38,120),threshold = 500, x_margin = 20, y_margin = 20, r_margin = 20,
            r_min = 3, r_max = 25, r_step = 5):
        area = (c.x()-c.r(), c.y()-c.r(), 2*c.r(), 2*c.r())#area为识别到的圆的区域，即圆的外接矩形框
        statistics = img.get_statistics(roi=area)#像素颜色统计
        #print(statistics)

        if 0<statistics.l_mode()<100 and -20<statistics.a_mode()<20 and 10<statistics.b_mode()<50:#if the circle is red
            img.draw_circle(c.x(), c.y(), c.r(), color = (0, 255, 0))#识别到的黄色圆形用红色的圆框出来
            print(f'该卵为好卵')
            Kv_switch.high()#继电器关闭
        else:
            img.draw_circle(c.x(),c.y(),c.r(), color = (255, 0, 0))
            print(f'为坏卵，准备吸收')
            i = 1
            #判断光电传感器是否被触发，触发则开启继电器
            while（i == 1）:
                if Sensing == 1:
                    Kv_switch.low()#继电器打开
                    delay(200)
                    Kv_switch.high()
                    i = 0

    #print("FPS %f" % clock.fps())
