import zmq

def shutdown(socket):
	## Shutdown brain
	socket.send_json({'cmd':'shutdown'})
	msg = socket.recv()
	print(msg)

def get_config(socket):
	## Get camera configuration
	socket.send_json({'cmd':'config'})
	metadata = socket.recv_json()
	return metadata

def set_config(socket,config={}):
	## Change camera configuration
	# e.g., config={'exposure':50000,'gain':10.0,'height':736,'width':1014}
	socket.send_json({'cmd':'set params',**config})
	msg = socket.recv()
	print(msg)

def live_preview(socket,frames,interval_sec):
	## Live preview
	# e.g., frames = 1000
	# e.g., interval_sec = .001 ## definitely cannot go faster than this
	import numpy as np
	import matplotlib.pyplot as plt
	metadata = get_config(socket)
	fig,ax = plt.subplots(1)
	im = None
	for _ in range(frames):
		plt.pause(interval_sec)
		socket.send_json({'cmd':'snap'})
		msg = socket.recv()
		img = np.frombuffer(msg,dtype=metadata['dtype'])
		img = img.reshape(metadata['shape'])
		if im is None:
			im = ax.imshow(img)
		else:
			im.set_data(img)

def timelapse(socket,filename,timepoints):
	## Timelapse
	# e.g., filename = 'special_timelapse'
	# e.g., timepoints = np.arange(20)*.05
	socket.send_json({'cmd':'timelapse', 'filename':filename, 'timepoints':timepoints.tolist()})
	msg = socket.recv()
	print(msg)

def clean_timelapse(socket):
	socket.send_json({'cmd':'clean timelapse'})
	msg = socket.recv()
	print(msg)

def get_file(socket,filename,outname=None):
	## Get file
	# e.g., filename = 'special_timelapse.txt'
	# outname for alternative name, if None it uses filename
	socket.send_json({'cmd':'get file','filename':filename})
	if outname is None:
		outname = filename
	with open(outname,'wb') as f:
		f.write(socket.recv())

def npy_to_tif(filename,data):
	## e.g., photometric = 'minisblack' or 'rgb' for b&w or color, respectively
	import tifffile as tf
	if data.shape[-1] == 3:
		photometric='rgb'
	else:
		photometric='minisblack'
	tf.imwrite(filename, data, photometric=photometric)


def get_timelapse(socket,filename,outname=None):
	## Get all timelapse files
	# e.g., filename = 'special_timelapse'
	# outname for alternative name, if None it uses filename
	get_file(socket,filename+'.npy',outname+'.npy')
	get_file(socket,filename+'.txt',outname+'.txt')

def connect(ip_target='localhost',port=5555):
	#### Connect to brain on ip_target
	# e.g., localhost='192.168.0.126'
	import time
	time.sleep(.5) ## let the brain start in case this is run at the same time....
	context = zmq.Context()
	socket = context.socket(zmq.REQ)
	socket.connect('tcp://%s:%d'%(ip_target,port))
	return context,socket

if __name__=='__main__':
	import numpy as np
	import matplotlib.pyplot as plt

	context,socket = connect('localhost',5555)

	timelapse(socket,'test_timelapse',np.arange(20)*.05)
	get_timelapse(socket,'test_timelapse','recvd_timelapse')

	## check
	d = np.load('recvd_timelapse.npy')
	print(d.shape)
	plt.imshow(d.mean(0))
	plt.show()
	with open('recvd_timelapse.txt','r') as f:
		print(f.read())

	# live_preview(socket,1000,.001)
	context.destroy()
