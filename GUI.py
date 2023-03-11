
from tkinter import filedialog, dialog
from tkinter import *  
import os
import os.path as path
import cv2
import glob
import numpy
from PIL import Image, ImageTk
import numpy as np
from PIL import Image, ImageDraw,ImageFont
import json
import collections
class ClassifyGUI():
	def __init__(self,config_file,root): 
		self.root = root

		with open(config_file,'r') as f:
			self.config = json.load(f)
		self.root.geometry(str(self.config['GUIResolution'][0])+'x'+str(self.config['GUIResolution'][1]))
		self.large_image_size = [int(self.config['RelativeLayoutImageView'][0]*self.config['GUIResolution'][0]),int(self.config['RelativeLayoutImageView'][1]*self.config['GUIResolution'][1])]
		self.small_image_size = [int(self.config['RelativeLayoutBirdView'][0]*self.config['GUIResolution'][0]),int(self.config['RelativeLayoutBirdView'][1]*self.config['GUIResolution'][1])]
		self.class_list = self.config['classList']
		self.image_list = []
		self.image_id= 0
		self.bird_id = 0
		self.cur_bbox = []
		self.use_prediction = False # This flag is used to reflect whether to use detection results to classify.
		self.filter_class = False # when enable, skip the boxes that has class id

		self.config_UI()
	
	def config_UI(self):# GUI configuration layout
		menubar = Menu(self.root) 
		filemenu = Menu(menubar,tearoff=0)  
		filemenu.add_command(label="open_image_dir",command = self.open_image_folder)
		filemenu.add_command(label="open_label_dir",command = self.open_label_folder)
		filemenu.add_command(label="open_detection_dir",command = self.open_detection_folder)
		filemenu.add_command(label="load_custom_settings",command = self.load_custom_settings)
		filemenu.add_separator()  
		filemenu.add_command(label="Exit", command=root.quit)  
		menubar.add_cascade(label="Open", menu=filemenu)  
		helpmenu = Menu(menubar, tearoff=0)  
		helpmenu.add_command(label="About", command=about)  
		menubar.add_cascade(label="Help", menu=helpmenu)



		self.root.config(menu=menubar)
		self.LargeImage = Image.new('RGB', (self.large_image_size[0],self.large_image_size[1]))
		self.largePhoto = ImageTk.PhotoImage(self.LargeImage)
		Label(self.root, image=self.largePhoto,width=self.large_image_size[0],height =self.large_image_size[1]).grid(row=0, column=0,rowspan = 20,columnspan=2,sticky=W+E+N+S)
		self.SmallImage = Image.new('RGB', (self.small_image_size[0],self.small_image_size[1]))
		self.smallPhoto = ImageTk.PhotoImage(self.SmallImage)
		Label(self.root, image=self.smallPhoto,width=self.small_image_size[0],height =self.small_image_size[1]).grid(row=0, column=3,rowspan = 5,columnspan=1,sticky=W+E+N+S)
		for idx,class_name in enumerate(self.class_list):
			Button(self.root,width=25,height=2,text =class_name,command = lambda class_name = class_name: self.create_classification(correct = True,label = class_name)).grid(row = idx, column = 4,columnspan=1)
		Button(self.root,width=25,height=2,text = "Not Bird",command = lambda: self.create_classification(correct = False,label = 'WrongAnno'),fg='red').grid(row = idx+1, column = 4,columnspan=1)
		Button(self.root,width=25,height=2,text = "Unknown",command = lambda: self.create_classification(correct = True,label = 'Not_Sure'),fg='red').grid(row = idx+2, column = 4,columnspan=1)
		Button(self.root,width=25,height=4,text = "Next_Image",command = lambda: self.switch_image('next'),fg='blue').grid(row = idx+3, column = 4,columnspan=1)
		Button(self.root,width=25,height=4,text = "Prev_Image",command = lambda: self.switch_image('prev'),fg='blue').grid(row = idx+4, column = 4,columnspan=1)
		Button(self.root,width=25,height=4,text = "Next_Bird",command = lambda: self.switch_box('next'),fg='green').grid(row = idx+3, column = 3,columnspan=1)
		Button(self.root,width=25,height=4,text = "Prev_Bird",command = lambda: self.switch_box('prev'),fg='green').grid(row = idx+4, column = 3,columnspan=1)
		Label(self.root, height=2, width=30,text = "Blue: pre-labeled",fg='blue').grid(row = idx+2, column = 3,columnspan=1)	
		Label(self.root, height=2, width=30,text = "Yellow: selected",fg='yellow').grid(row = idx+1, column = 3,columnspan=1)	
		Label(self.root, height=2, width=30,text = "Red: unlabeled",fg='red').grid(row = idx, column = 3,columnspan=1)
		Checkbutton(self.root, text='filter class', variable=self.filter_class, onvalue=True, offvalue=False).grid(row = idx-1, column = 3,columnspan=1)	
	
	def open_image_folder(self):
		self.image_id = 0
		file_path = filedialog.askdirectory(title=u'open_folder', initialdir=(os.path.expanduser('/home/robert/Models/model_inference_gui/example_images/Bird_drone/15m')))
		self.image_list = sorted(glob.glob(file_path+'/*.jpg')+glob.glob(file_path+'/*.JPG')+glob.glob(file_path+'/*.png'))
		self.display_image()

	def open_label_folder(self):
		file_path = filedialog.askdirectory(title=u'open_folder', initialdir=(os.path.expanduser('/home/robert/Models/model_inference_gui/example_images/Bird_drone/15m')))
		self.label_dir = file_path
		self.use_prediction = False
		self.load_current_annotation()
		self.display_image()

	def open_detection_folder(self):
		file_path = filedialog.askdirectory(title=u'open_folder', initialdir=(os.path.expanduser('/home/robert/Models/model_inference_gui/example_images/Bird_drone/15m_results/classification-results')))
		self.label_dir = file_path
		self.use_prediction = True
		self.load_current_annotation()
		self.display_image()

	def load_custom_settings(self):#custom settings that allow operations such as filter target class of birds
		file_path = filedialog.askopenfilename(title=u'open_custom_settings', initialdir=(os.path.expanduser('./')))
		with open(file_path,'r')as f:
			self.custom_config = json.load(f)

		print (self.custom_config)
	
	def display_image(self):
		self.LargeImage = Image.open(self.image_list[self.image_id])
		self.draw_annotation()#draw bbox
		self.largePhoto = ImageTk.PhotoImage(self.LargeImage.resize((self.large_image_size[0],self.large_image_size[1]),resample=0))
		self.smallPhoto = ImageTk.PhotoImage(self.SmallImage.resize((self.small_image_size[0],self.small_image_size[1]),resample=0))
		Label(root, image=self.largePhoto,width=self.large_image_size[0],height =self.large_image_size[1]).grid(row=0, column=0,rowspan = 20,columnspan=2,sticky=W+E+N+S)
		Label(root, image=self.smallPhoto,width=self.small_image_size[0],height =self.small_image_size[1]).grid(row=0, column=3,rowspan = 5,columnspan=1,sticky=W+E+N+S)
		self.draw_annotation()
		print (self.cur_bbox)

	def draw_annotation(self):
		draw = ImageDraw.Draw(self.LargeImage)
		if (self.cur_bbox!=[]):
			current_box = self.cur_bbox[self.bird_id]
			length = max(abs(current_box[3]-current_box[1]),abs(current_box[4]-current_box[2]))
			center = [(current_box[3]+current_box[1])/2,(current_box[4]+current_box[2])/2]
			self.SmallImage = self.LargeImage.crop((center[0]-length/2,center[1]-length/2,center[0]+length/2,center[1]+length/2))
			draw.rectangle((current_box[1],current_box[2],current_box[3],current_box[4]),outline='yellow',width = 5)
			Label(root, height=2, width=30,text = "Label: {}".format(current_box[0]),fg='blue').grid(row = 6, column = 3,columnspan=1)
		for idx,box in enumerate(self.cur_bbox):
			if (idx==self.bird_id):
				continue
			if (box[0]=='Bird'):
				draw.rectangle((box[1],box[2],box[3],box[4]),outline='red',width = 5)
				Label(root, height=2, width=30,text = "Label: Bird",fg='red').grid(row = 6, column = 3,columnspan=1)
			else:
				draw.rectangle((box[1],box[2],box[3],box[4]),outline='blue',width = 5)
				
		

	def save_current_annotation(self,label = None, correct = True):# save the current annotations, and also move to next
		if(not os.path.isdir(os.path.split(self.result_file)[0])):
			os.mkdir(os.path.split(self.result_file)[0])
		current_box = self.cur_bbox[self.bird_id]
		bird_w_label = False
		if(path.exists(self.result_file)):
			with open(self.result_file, "r") as f1,open("%s.bak" % self.result_file, "w") as f2:
				for line in f1.readlines():
					box = [int(i) for i in line.split(' ')[2:]]
					if (collections.Counter(current_box) == collections.Counter(box)):
						bird_w_label = True
						f2.writelines('{},{},{},{},{}\n'.format(label,current_box[0],current_box[1],current_box[2],current_box[3]))
					else:
						f2.writelines(line)
				if (bird_w_label == False):
					f2.writelines('{},{},{},{},{}\n'.format(label,current_box[0],current_box[1],current_box[2],current_box[3]))
			os.remove(self.result_file)
			os.rename("%s.bak" % self.result_file, self.result_file)
		else:
			with open(self.result_file, "w") as f:
				f.writelines('{},{},{},{},{}\n'.format(label,current_box[0],current_box[1],current_box[2],current_box[3]))
		self.switch_box('next')

	def load_current_annotation(self):#Load the gt/detection file for current image
		self.cur_bbox = []
		bird_w_label = False
		image_name = os.path.split(self.image_list[self.image_id])[1]
		self.detection_file = os.path.join(self.label_dir,image_name.split('.')[0]+'.txt')
		self.result_file = os.path.join(os.path.split(self.image_list[self.image_id])[0],'result_labels',image_name.replace('.JPG','.txt'))
	
		with open(self.detection_file,'r') as f:
			detection_data = f.readlines()
		for data in detection_data:
			if(self.use_prediction):
				box = [data.split(',')[0]]+[int(i) for i in data.split(',')[2:]]+[float(data.split(',')[1])]
			else:
				box = [data.split(',')[0]]+[int(i) for i in data.split(',')[1:]]+[1.0]
			self.cur_bbox.append(box)
		if (self.cur_bbox!=[]):
			current_box = self.cur_bbox[self.bird_id]
			length = max(abs(current_box[3]-current_box[1]),abs(current_box[4]-current_box[2]))
			center = [(current_box[3]+current_box[1])/2,(current_box[4]+current_box[2])/2]
			self.SmallImage = self.LargeImage.crop((center[0]-length/2,center[1]-length/2,center[0]+length/2,center[1]+length/2))
		#if there pre-existing some result file, pick from what is left
		if(path.exists(self.result_file)):
			current_box = []
			with open(self.result_file,'r') as f:
				result_data = f.readlines()
			for data in result_data:
				box = [data.split(',')[0]]+[int(i) for i in data.split(',')[2:]]
				self.cur_bbox.append(box)

	
	def switch_image(self,direction = 'next'): # switch to the next large image
		if (direction=='next'):
			self.image_id= min(len(self.image_list)-1,self.image_id+1)
		else:
			self.image_id=max(0,self.image_id-1)
		self.bird_id = 0
		self.load_current_annotation()
		self.display_image()
	
	def switch_box(self,direction = 'next'):#switch to the next bounding box annotation
		if (direction=='next'):
			self.bird_id= min(len(self.cur_bbox)-1,self.bird_id+1)
		else:
			self.bird_id=max(0,self.bird_id-1)
		self.display_image()

def about():
	print ('open')


if __name__ == '__main__':
	root = Tk()
	root.title('bird_classfiy')
	root.geometry('400x200')
	
	config_file = './bird_label_config.json'
	ClassifyGUI(config_file,root)
	root.mainloop()
