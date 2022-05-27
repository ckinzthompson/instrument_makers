# brain
import zmq
import time
import os
import json
import numpy as np

def log(msg):
	print(msg)

def _camera_metadata(camera):
	return dict(name=camera.name,dtype=str(camera.dtype),shape=camera.shape)

def get_config(camera,socket):
	metadata = _camera_metadata(camera)
	socket.send_json(metadata)
	log('got config')

def get_snap(camera,socket):
	img = camera.snap()
	socket.send(img)
	log('got snap')

def set_params(params,camera,socket):
	msg = camera.set_params(params)
	socket.send_string('okay')
	log('set params - %s'%(params))

def timelapse(params,camera,socket):
	if not 'timepoints' in params:
		### this should be a numpy array of seconds after which to take a picture
		socket.send_string('timelapse input missing: timepoints')
		return
	if not 'filename' in params:
		### this should be the string for the .npy data without the npy
		socket.send_string('timelapse input missing: filename')
		return
	socket.send_string('timelapse started') ## frees up the control computer to log out

	metadata = _camera_metadata(camera)
	timepoints = np.array(params['timepoints']) ## an np.ndarray of timepoints to take a picture after
	timepoints.sort()
	print(params)
	npics = timepoints.size
	data = np.zeros((npics, *metadata['shape']), dtype=metadata['dtype'])

	t0 = time.time()
	metadata['start time'] = t0
	for i in range(npics):
		while True:
			dt = time.time() - t0
			if dt >= timepoints[i]:
				break
		data[i] = camera.snap()
		metadata['time_%d'%(i)] = dt
		np.save(params['filename']+'.npy',data[:i+1])
		with open(params['filename']+'.txt', 'w', encoding='utf-8') as f:
			json.dump(metadata, f, ensure_ascii=False, indent=4)
		log('took picture %d'%(i))

def get_file(params,socket):
	if not 'filename' in params:
		socket.send_string('file input missing: filename')

	fname = params['filename']
	if os.path.isfile(fname): ## only allow in current directory for safety
		head,tail = os.path.split(fname)
		if os.path.isfile(tail):
			log('file in cwd')
			with open(tail,'rb') as f:
				contents = f.read()
				socket.send(contents)
			log('sent file')
			return
	socket.send(b'')
	log('file send issue')

def clean_timelapse(params,socket):
	fns = os.listdir('./')
	for fn_npy in fns:
		if fn_npy.endswith('.npy'):
			for fn_txt in fns:
				if fn_txt.endswith('.txt') and fn_txt.startswith(fn_npy[:-4]):
					os.remove(fn_txt)
					os.remove(fn_npy)
					break
	socket.send_string('Files removed')

def unknown(socket):
	socket_brain.send_string('unknown')
	log('unknown command')

def connect(ip_target='*',port=5555):
	context = zmq.Context()
	socket = context.socket(zmq.REP)
	socket.bind('tcp://%s:%d'%(ip_target,port))
	return context,socket

def brain_mainloop(context,socket,camera):
	####### Brain Control loop
	while True:
		## Get the next command
		message = socket.recv_json()
		cmd = message['cmd']

		## Run the command
		if cmd == 'snap':
			get_snap(camera,socket)
		elif cmd == 'config':
			get_config(camera,socket)
		elif cmd == 'set params':
			set_params(message,camera,socket)
		elif cmd == 'timelapse':
			timelapse(message,camera,socket)
		elif cmd == 'clean timelapse':
			clean_timelapse(message,socket)
		elif cmd == 'shutdown':
			socket.send_string('Shutting down')
			break
		elif cmd == 'get file':
			get_file(message,socket)
		else:
			unknown(socket)

	context.destroy()
	log('Shutdown')


if __name__=='__main__':
	from cameras import fake_camera

	context,socket = connect('*',5555)
	camera = fake_camera()
	brain_mainloop(context,socket,camera)
