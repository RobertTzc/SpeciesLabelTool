
from tkinter import filedialog, dialog
from tkinter import *  
import os
import os.path as path
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
		self.class_list = self.config['class_list']
		self.image_list = []
		self.image_id= 0
		self.bird_id = 0
		self.bbox = []
		self.config_UI()
	def config_UI(self):
		menubar = Menu(self.root) 
		filemenu = Menu(menubar,tearoff=0)  
		filemenu.add_command(label="open_dir",command = self.open_folder)  
		filemenu.add_separator()  
		filemenu.add_command(label="Exit", command=root.quit)  
		menubar.add_cascade(label="File", menu=filemenu)  
		helpmenu = Menu(menubar, tearoff=0)  
		helpmenu.add_command(label="About", command=about)  
		menubar.add_cascade(label="Help", menu=helpmenu)    
		self.root.config(menu=menubar)
		self.LargeImage = Image.new('RGB', (self.large_image_size[0],self.large_image_size[1]))
		self.largePhoto = ImageTk.PhotoImage(self.LargeImage)
		Label(root, image=self.largePhoto,width=self.large_image_size[0],height =self.large_image_size[1]).grid(row=0, column=0,rowspan = 20,columnspan=2,sticky=W+E+N+S)
		self.SmallImage = Image.new('RGB', (self.small_image_size[0],self.small_image_size[1]))
		self.smallPhoto = ImageTk.PhotoImage(self.SmallImage)
		Label(root, image=self.smallPhoto,width=self.small_image_size[0],height =self.small_image_size[1]).grid(row=0, column=3,rowspan = 3,columnspan=1,sticky=W+E+N+S)
		self.load_labels()
		Button(root,width=25,height=4,text = "Next_Image",command = lambda: self.switch_image('next'),fg='blue').grid(row = 7, column = 3,columnspan=1)
		Button(root,width=25,height=4,text = "Prev_Image",command = lambda: self.switch_image('prev'),fg='blue').grid(row = 8, column = 3,columnspan=1)
		Button(root,width=25,height=4,text = "Next_Bird",command = lambda: self.switch_box('next'),fg='green').grid(row = 9, column = 3,columnspan=1)
		Button(root,width=25,height=4,text = "Prev_Bird",command = lambda: self.switch_box('prev'),fg='green').grid(row = 10, column = 3,columnspan=1)
		Label(root, height=2, width=30,text = "Blue: pre-labeled",fg='blue').grid(row = 6, column = 3,columnspan=1)	
		Label(root, height=2, width=30,text = "Yellow: selected",fg='yellow').grid(row = 5, column = 3,columnspan=1)	
		Label(root, height=2, width=30,text = "Red: unlabeled",fg='red').grid(row = 4, column = 3,columnspan=1)	

	def load_labels(self):
		for idx,class_name in enumerate(self.class_list.keys()):
			if ('RED' in class_name):
				class_name = class_name.replace('RED','')
				Button(self.root,width=25,height=2,text =class_name,command = lambda class_name = class_name: self.create_classification(label = class_name),fg='red').grid(row = idx, column = 4,columnspan=1)
			else:
				if (self.class_list[class_name] == {}):
					Button(self.root,width=25,height=2,text =class_name,command = lambda class_name = class_name: self.create_classification(label = class_name)).grid(row = idx, column = 4,columnspan=1)
				else:
					Button(self.root,width = 25,height=2,text = class_name,command = lambda class_name=class_name: self.diag_other_opt(class_name),fg = 'green').grid(row = idx, column = 4,columnspan=1)

	def diag_other_opt(self,class_name): 
		tp = Toplevel()
		idx = 0
		candidates = self.class_list[class_name]
		for candidate in candidates.keys():
			if (candidates[candidate]=={}):
				Button(tp,width = 25,height=2,text = candidate,command = lambda candidate = candidate: self.create_classification(candidate,True,[tp])).grid(row = idx, column =1)
			else:
				Label(tp,width = 25,height=2,text = candidate).grid(row = idx, column =1)
				for item in candidates[candidate].keys():
					if (candidates[candidate][item]==[]):
						if ('fill in species' in item):
							tmp=Entry(tp,width=25)
							tmp.grid(row = idx, column =1)
							Button(tp,width = 25,height=2,text = 'Customize',command = lambda text_box = tmp: self.getData(text_box,tp)).grid(row = idx, column =2)
						else:
							Button(tp,width = 25,height=2,text = item,command = lambda item = item: self.create_classification(item,True,[tp])).grid(row = idx, column =2)
					else:
						global sex 
						Button(tp,width = 25,height=2,text = item,command = lambda item = item,candidates = candidates,candidate = candidate:self.choose_sex(item,candidates,candidate,tp)).grid(row = idx, column =2)
		
					idx+=1
			idx+=1	
		Button(tp,text = "Finish",command =lambda:tp.destroy()).grid(row = idx, column =1)
		return

	def getData(self,text_box,tp):
		text = text_box.get()
		self.create_classification(text,True,[tp])

	def choose_sex(self,item,candidates,candidate,tp):
		tp2 = Toplevel()
		for i in candidates[candidate][item]:
			Button(tp2,width = 25,height=2,text = i,command = lambda i = i,item = item: self.create_classification(item+'_'+i,True,[tp2,tp])).pack()
		Button(tp2,text = "Finish",command =lambda:tp2.destroy()).pack()

	def open_folder(self):
		self.image_id = 0
		self.file_path = filedialog.askdirectory(title=u'open_folder', initialdir=(os.path.expanduser('/home/robert/project5_inference_height')))
		self.image_list = sorted(glob.glob(self.file_path+'/*.jpg')+glob.glob(self.file_path+'/*.JPG')+glob.glob(self.file_path+'/*.png'))
		self.display_images()

	def display_images(self):
		self.LargeImage = Image.open(self.image_list[self.image_id])
		self.load_annotation()#draw bbox
		self.largePhoto = ImageTk.PhotoImage(self.LargeImage.resize((self.large_image_size[0],self.large_image_size[1]),resample=0))
		self.smallPhoto = ImageTk.PhotoImage(self.SmallImage.resize((self.small_image_size[0],self.small_image_size[1]),resample=0))
		Label(root, image=self.largePhoto,width=self.large_image_size[0],height =self.large_image_size[1]).grid(row=0, column=0,rowspan = 20,columnspan=2,sticky=W+E+N+S)
		Label(root, image=self.smallPhoto,width=self.small_image_size[0],height =self.small_image_size[1]).grid(row=0, column=3,rowspan = 3,columnspan=1,sticky=W+E+N+S)
	
	def create_classification(self,label = None,turnNext = True,tp_list = None):
		print (label)
		self.save_anno(label)
		if (turnNext):
			self.switch_box('next')
		if (tp_list):
			for t in tp_list:
				t.destroy()


	def save_anno(self,label):
		if(not os.path.isdir(os.path.split(self.result_file)[0])):
			os.mkdir(os.path.split(self.result_file)[0])
		current_box = self.bbox[self.bird_id]
		bird_exist = False
		if(path.exists(self.result_file)):
			with open(self.result_file, "r") as f1,open("%s.bak" % self.result_file, "w") as f2:
				for line in f1.readlines():
					box = [int(i) for i in line.split(',')[2:]]
					if (collections.Counter(current_box) == collections.Counter(box)):
						bird_exist = True
						f2.writelines('bird,{},{},{},{},{}\n'.format(label,current_box[0],current_box[1],current_box[2],current_box[3]))
					else:
						f2.writelines(line)
				if (bird_exist == False):
					f2.writelines('bird,{},{},{},{},{}\n'.format(label,current_box[0],current_box[1],current_box[2],current_box[3]))
			os.remove(self.result_file)
			os.rename("%s.bak" % self.result_file, self.result_file)
		else:
			with open(self.result_file, "w") as f:
				f.writelines('bird,{},{},{},{},{}\n'.format(label,current_box[0],current_box[1],current_box[2],current_box[3]))



	def load_annotation(self):
		self.bbox = []
		bird_exist = False
		draw = ImageDraw.Draw(self.LargeImage)
		image_name = os.path.split(self.image_list[self.image_id])[1]
		self.detection_file = os.path.join(os.path.split(self.image_list[self.image_id])[0].replace('image','detection-results'),image_name.replace('.JPG','.txt'))
		self.result_file = os.path.join(os.path.split(self.image_list[self.image_id])[0].replace('image','refinment_results'),image_name.replace('.JPG','.txt'))
	
		with open(self.detection_file,'r') as f:
			detection_data = f.readlines()
		for data in detection_data:
			box = [int(i) for i in data.split(' ')[2:]]
			self.bbox.append(box)
		if (self.bbox!=[]):
			current_box = self.bbox[self.bird_id]
			length = max(abs(current_box[2]-current_box[0]),abs(current_box[3]-current_box[1]))
			center = [(current_box[2]+current_box[0])/2,(current_box[3]+current_box[1])/2]
			self.SmallImage = self.LargeImage.crop((center[0]-length/2,center[1]-length/2,center[0]+length/2,center[1]+length/2))
		for box in self.bbox:
			draw.rectangle((box[0],box[1],box[2],box[3]),outline='red',width = 5)
		if(path.exists(self.result_file)):
			
			with open(self.result_file,'r') as f:
				result_data = f.readlines()
			for data in result_data:
				box = [int(i) for i in data.split(',')[2:]]
				if (collections.Counter(current_box) == collections.Counter(box)):
					bird_exist = True
					Label(root, height=2, width=30,text = "Label: "+data.split(',')[1],fg='black').grid(row = 3, column = 3,columnspan=1)
				category = data.split(',')[1]
				draw.text(xy=(box[0]-5,box[1]-5), text=category, fill=(0, 255, 255), )
				draw.rectangle((box[0],box[1],box[2],box[3]),outline='blue',width = 5)
		if (self.bbox!=[]):
			box = self.bbox[self.bird_id]
			draw.rectangle((box[0],box[1],box[2],box[3]),outline='yellow',width = 5)
		if (bird_exist == False):
			Label(root, height=2, width=30,text = "Label: unlabeled",fg='black').grid(row = 3, column = 3,columnspan=1)
	def switch_image(self,direction = 'next'):
		if (direction=='next'):
			self.image_id= min(len(self.image_list)-1,self.image_id+1)
		else:
			self.image_id=max(0,self.image_id-1)
		self.bird_id = 0
		self.display_images()
	def switch_box(self,direction = 'next'):
		if (direction=='next'):
			self.bird_id= min(len(self.bbox)-1,self.bird_id+1)
		else:
			self.bird_id=max(0,self.bird_id-1)
		self.display_images()

def about():
	print ('open')


if __name__ == '__main__':
	root = Tk()
	root.title('bird_classfiy')
	root.geometry('400x200')
	
	config_file = './new_category.json'
	ClassifyGUI(config_file,root)
	root.mainloop()
