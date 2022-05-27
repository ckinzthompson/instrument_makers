import numpy as np
import remote_rpi_camera as rrc

context,socket = rrc.control.connect('localhost',5555)

config={'exposure':5.,'gain':10.0}
rrc.control.set_config(socket,config)
rrc.control.live_preview(socket,1000,.001)

rrc.control.timelapse(socket,'test_timelapse',np.arange(20)*.01)
rrc.control.get_timelapse(socket,'test_timelapse','recvd_timelapse')

## check
import matplotlib.pyplot as plt
d = np.load('recvd_timelapse.npy')
print(d.shape)
plt.imshow(d.mean(0))
plt.show()
with open('recvd_timelapse.txt','r') as f:
	print(f.read())

d = np.load('recvd_timelapse.npy')
rrc.control.npy_to_tif('recvd_timelapse.tif',d)

rrc.control.clean_timelapse(socket)


context.destroy()
