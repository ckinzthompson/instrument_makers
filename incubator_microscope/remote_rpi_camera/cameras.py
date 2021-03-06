# cameras.py
import numpy as np

class libcamera_camera(object):
	def __init__(self):
		from picamera2.picamera2 import Picamera2
		self.picam2 = Picamera2()
		self.picam2.start_preview()
		self.picam2.configure(self.picam2.preview_configuration())
		self.picam2.start()
		self.picam2.stop()

		self.shape = [640,480,3]
		self.shape = [4056,3040,3]
		self.dtype = 'uint8'
		self.gain = 1.0
		self.exposure = 10000 #us
		self.name = 'libcamera raspberry pi cam'
		self.set_params({})
		self.last = None
		self.snap()

	def __del__(self):
		self.picam2.close()
		del(self)

	def snap(self):
		try:
			# t0 = time.time() ## full res takes ~ 0.2 sec. limited by transfer .. yeah it's like 37 Mb
			self.last = self.picam2.capture_array()
			# t1 = time.time()
			# print('snap',t1-t0)
		except:
			self.last = np.zeros(self.shape,dtype=self.dtype)
		return self.last

	def set_params(self,params):
		msg = []
		if 'name' in params:
			newname = str(params['name'])
			msg.append('name: %s > %s'%(self.name,newname))
			self.name = newname
		if 'width' in params:
			newwidth = int(params['width'])
			msg.append('width: %d > %d'%(self.shape[0],newwidth))
			self.shape[0] = newwidth
		if 'height' in params:
			newheight = int(params['height'])
			msg.append('height: %d > %d'%(self.shape[1],newheight))
			self.shape[1] = newheight
		if 'exposure' in params:
			newexposure = int(params['exposure'])
			msg.append('exposure: %d > %d'%(self.exposure,newexposure))
			self.exposure = newexposure
		if 'gain' in params:
			newgain = float(params['gain'])
			msg.append('gain: %d > %d'%(self.gain,newgain))
			self.gain = newgain
		self.picam2.stop()
		capture_config = self.picam2.still_configuration(main = {"size" : (self.shape[1], self.shape[0]), "format" : "BGR888"})
		self.picam2.configure(capture_config)
		self.picam2.start({"ExposureTime":self.exposure,"AnalogueGain":self.gain})
		return '\n'.join(msg)

class raspi_camera(object):
	def __init__(self):
		import subprocess
		self.subprocess = subprocess
		self.shape = (1944,2592,3)
		#self.shape = (640,480,3)
		self.dtype = 'uint8'
		self.gain = 1.0
		self.exposure = 10000 #us
		self.name = 'legacy raspberry pi cam'
		self.last = None
		self.snap()

	def snap(self):
		try:
			cmd = ('raspiyuv -rgb -t 1 -o - -n -w %d -h %d -ex off -ag %f -dg 1.0 --shutter %d'%(self.shape[1],self.shape[0],self.gain,self.exposure)).split(' ')
			self.last = np.frombuffer(self.subprocess.run(cmd, stdout=self.subprocess.PIPE).stdout[:self.shape[0]*self.shape[1]*self.shape[2]],dtype='uint8')
			self.last = self.last.reshape((self.shape[0],self.shape[1],self.shape[2]))
		except:
			self.last = np.zeros(self.shape,dtype=self.dtype)
		return self.last

	def set_params(self,params):
		msg = []
		if 'name' in params:
			newname = str(params['name'])
			msg.append('name: %s > %s'%(self.name,newname))
			self.name = newname
		if 'exposure' in params:
			newexposure = int(params['exposure'])
			msg.append('exposure: %d > %d'%(self.exposure,newexposure))
			self.exposure = newexposure
		if 'gain' in params:
			newgain = float(params['gain'])
			msg.append('gain: %d > %d'%(self.gain,newgain))
			self.gain = newgain
		return '\n'.join(msg)


class fake_camera(object):
	def __init__(self):
		self.shape = (64,64)
		self.dtype = 'uint16'
		p = p = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x130\x16\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\rM\x8c\x86\x84#\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03,\x80\x85hcg\x84\x17\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0eW\x90nhopfrh\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02$}\x81dmpppo]\x884\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08F\x8fmfopppppj`\x80\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16k\x88ckpppppppp`\x82?\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02+\x85vbnpppppppppl_\x80\x0b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07H\x8egfoppppppppppp_\x855\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0ee\x86`jpppppppppppppjes\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x14xz_mppppppppppppppo[\x8d\x1c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0eyw_nppppppppppppppppdwM\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07ez^npppppppppppppppppl^|\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01B\x88YnppppppppppppppppppoZ\x8c\x19\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11\x88Xippppppppppppppppppppb\x7f;\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01D}[oppppppppppppppppppppiie\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04t^ipppppppppppppppppppppm[\x83\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1d\x8fXnpppppppppppppppppppppoX\x8b\x12\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\t|lJcmoppppppppppppppppppppZ\x8a \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00(\x8bTf^Y]floppppppppppppppppp\\\x83*\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02]obppmg]WYajnpppppppppppppp^\x80,\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\t\x85Xkpppppmg\\SSZdknpppppppppp]\x84)\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1b\x8eWoppppppppni`UOR[dknpppppp[\x8b\x1b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x000\x82^ppppppppps\x8f\x9e\x95zg\\SOS[cjnol^\x84\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x15lcJelopppppp\x8e\xa7\x7f\x92\xaa\x8bpolg`YUVYOmf\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05&]\x82Q\x15Z\x80fZ`hmopp\x8a|XVo\xb1tpppponmjekw\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07WyD\x18\x03(\x96\xd4\xb7\x99\x94{\\[ciq\x93\xa2\x8a\x80\xa7rppppppppoui\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01@s.\n\x00\x04d\xb0\xc6\xcf\xf6\xf6\xa4J\\\x7fdccw\x8a\x84upppppppppk\x85A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05uf\xa2,\x00\x1e\x9f\xc0\xbe\xea\xff\xde7\x06\x1e\xb0\xb6\xc5\xb6\x99}h`gknppppppf\x8f\x19\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04x\x9b\xc1-\x08u\xba\xce\xcd\xc7\xf7\xdf9\x06 \xbd\xc9\xd3\xdf\xde\xd7\xb2\xa1\x86^llgknnlky\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06y\xc1\xc4Wg\xaf\xb6\xd8\xdd\xc7\xc0\xdb\xa7d\x90\xd0\xbb\xda\xdf\xdf\xcd\xcd\xc07\x1do\xd6\xa8\x82\x81cE|@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04I\xaa\xc1\xc8\xbd\x81r\xb6\xdc\xdf\xde\xd5\xc4\xba\xb4\xb8\xc2\xc6\xbc\xcb\xdd\xca\xd4\x92\x0c\x02?\xe8\xf8\xc1\xca\x8f%j3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x003\xac\xaf\xc5\xcb\xc8\xb4\x8e\xb5\xdb\xdf\xdf\xdf\xdf\xdd\xdc\xdd\xbeSBC\xa1\xd6\xba\xb18"\x7f\xf6\xff\xd6\xbd\x8b\x1a>f\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06|\xb4\xca\xc7\xc5\xda\xba\x96\xb5\xcb\xde\xdf\xdf\xdf\xd3\xc1\xdc\xa2\'&\x1aK\xd2\xd4\xb8\xab\xb6\xe6\xf3\xe3\xbb\xb5\x8a\x10\rv=\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x9c\xb5\xc7\xc0\xd6\xdc\xbcdn\xb6\xc8\xda\xdf\xdf\xd6\x8a\xac\xc5b+*r\xd8\xde\xdb\xcd\xbf\xbb\xbb\xc2\xd2\xab\x9a\x0b\x00\x1cxF\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04d\xb6\xc9\xd9\xdf\xdc\xbeu\x13R\xa9\xbc\xc9\xd6\xdd\xc2\x84\x94\xad\xa8\xae\xcb\xcb\xb6\xd0\xdf\xde\xdd\xdd\xde\xd3\xaf\xa7\n\x00\x00\x15r@\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0cv\xc3\xd1\xd6\xdd\xd1\xba^\x18P\xb9\xc6\x91\xa7\xc5\xb6\x8d\x8b\x8c\x8c\x86\x81\xaa\xd9\xdf\xdf\xdf\xdf\xdf\xc1\xb7\xa0\x10\x00\x00\x00\x1c\x80\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x82\xaf\xb5\xc9\xde\xd1\xbb\xa7\xb3\xbe\xc0ldr\x87\x96\x95\x96\xa0\xb6\xd0\xdd\xdf\xdf\xdf\xdf\xdf\xda\xb2\x87r>\x02\x00\x00\x0b\x80\x17\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x1ds\xb2\xcf\xde\xd0\xc6\xd4\xdb\xb7\\``bemy\x8b\x9e\xae\xc4\xd1\xd6\xd9\xdb\xd9\xc7\xaa-\x1f~?\x0e\x0bCn\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12\x87\xb2\xd2\xdd\xd8\xcb\xb5n[`````abcR\x86\xb8\xcc\xd1\xc7\xbb\x9b?\x03\x01\x1dh~~k\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1a\x8e\xb1\xb3\xaa\xb4\xafW_````````M\x90\xc0\xb8\xc6\xb8i\x1e\x02\x00\x00\x00\x04\x12\x15\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18q\x8fs\x8f\x80Z`````````R\x82\xd9\xda\xce\xbc\xb5\x90\x14\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x08!\x8fY_`````````WY\xb1\xc2\xd4\xdd\xd1\xb4/\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06ko\\``````````\\S\xb7\xaf\xb3\xd9\xd3\xb1$\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x016\x8bY```````````_K\x8f{\xc4\xdc\xc3\x99\r\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16\x8bc^````````````O\x8b\xbe\xd1\xd9\xb6i\x0b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08nrZ`````````````Wg\xbb\xd9\xd2\xb7\xaf\x85\x14\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00)\x89M_`````````````^I\x8a\xd9\xdd\xc7\xb5\xb2D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1e\x93aMZ_````````````R`\xbe\xda\xd1\xc6\xc0\x81\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x13\x81Q\x19)<LW\\^_``````^RQ\xcc\xcf\xc9\xc6\xc1s\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08lX\x11\x0c\r\x11\x1a&2=GMNONKE;,\'\x81\xc1\xa7\x8a`\x13\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1e\x81\x15\x0c\x0c\x0c\x0c\x0c\r\x0f\x17]k$ \x1d\x1a\x16\x12\x0e\x0c\x119|\x0c\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02-\x8d\x16\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x17\x9b\x99\x15\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c(|\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01;\x86G\r\x0c\x0c\x0c\x0c\x0c\x0c\x0b\x1e\x97\x8d\x14\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0cHj\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\t\t\t\t\nu3\r\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0b\x1c\x97\x8f\x15\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c%\x80=\x08\t\t\x07\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x13d\x83\x80\x81\x88}\xa7Q\r\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x19\x93\x971\x0c\x0c\x0c\x0c\x0c\x0b\x0b\x0c\x0fG\xa1\x88\x88\x85}g\'\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0ctdKLT\x9d\x96nsW(\x0e\x0c\x0c\x0c\x0c\x0c\x0c.\x81\x890\x0c\x0c\x0b\x0b\x0b\r\x13;~d\x91\xc2jNKY\x862\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00,zANMh\xbb\xbc\x9f\xc6\xc0\xa28"\x15\x0e\r\x0c\x0c)\x88\x91%\x0c\x0c\r\x14#4K\xad\xb0\xc1\xca\xaa\x95NI=A{\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00%\x8d\x96\xa4\x97\x9c\x9e\x9a\xb6\xa7\x98\xaa\x81}ug`#&U\x8a\x901\x168Vbio\x83\xaf\x94\xbe\xbe\xa6\xb1\xa8\xa3sWt\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05H\x89\x96\x98\x9a\x9e\xa3\xa9\xae\xb3\xb6\xb6\xb4\xb3\xac\x9c\x80\x89d+o\x84\x82\x98\xa2\xa5\xae\xb6\xb7\xb4\xb0\xb0\xad\xa8\xa1\x9a\x91\x89q\x1c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x0b\x17").222221-***%\x17\x03\x00\x07\x191DJMGDA;:6321-&\x17\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		self.parappa = np.frombuffer(p,dtype='uint8').reshape((64,64)).astype('double')/255.
		self.exposure = 50.
		self.name = 'parappa cam'
		self.last = None
		self.snap()
	def snap(self):
		self.last = np.random.poisson((self.parappa*10.+1.)*self.exposure).astype('uint16')
		return self.last
	def set_params(self,params):
		msg = []
		if 'exposure' in params:
			newexposure = float(params['exposure'])
			msg.append('exposure: %f > %f'%(self.exposure,newexposure))
			self.exposure = newexposure
		if 'name' in params:
			newname = str(params['name'])
			msg.append('name: %s > %s'%(self.name,newname))
			self.name = newname
		return '\n'.join(msg)


#######
if __name__=='__main__':
	# camera = raspi_camera()
	camera = fake_camera()
	# camera = libcamera_camera()

	import matplotlib.pyplot as plt
	plt.imshow(camera.snap())
	plt.show()
