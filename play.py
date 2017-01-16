# coding: utf-8
okno = ShutterManager('172.30.1.231')
okno.down()
if okno.is_in_position(100):
    okno.tilt()
else:
    print('Fail!')
