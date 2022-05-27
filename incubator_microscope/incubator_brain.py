import remote_rpi_camera as rrc

context,socket = rrc.brain.connect('*',5555)
camera = rrc.cameras.fake_camera()
rrc.brain.brain_mainloop(context,socket,camera)
