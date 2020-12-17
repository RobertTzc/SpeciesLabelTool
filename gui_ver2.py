
from tkinter import filedialog, dialog
from tkinter import *  
import os
import os.path as path
import tkinter
import glob
import numpy
from PIL import Image, ImageTk
import numpy as np
from PIL import Image, ImageDraw
root = Tk(className = 'Annotation label')  
root.geometry('1200x800')
 
file_path = ''
image_list = []
img = Image.new('RGB', (800,800))
specis_list = ['Mallard','Pintail','Green-winged teal','Gadwall','Shoveler','Widgeon','Canada Goose','Greater White-fronted Goose','Snow Goose']
current_id = 0
bbox = []
bird_index = 0
box_img = Image.new('RGB', (800,800))
annotated_bbox = []
def open_folder():
    '''
    打开文件
    :return:
    '''
    global file_path
    global file_text
    global current_id
    current_id = 0
    file_path = filedialog.askdirectory(title=u'open_folder', initialdir=(os.path.expanduser('/home/robert/project5_inference_height')))
    global image_list
    image_list = sorted(glob.glob(file_path+'\\*.JPG'))
    show_image()
    start_bird_box()

def open_file():
    '''
    打开文件
    :return:
    '''
    global image_list
    global current_id
    current_id = 0
    file_path = filedialog.askopenfilename(title=u'open_file', initialdir=(os.path.expanduser('/home/robert')))
    if file_path is not None:
    	image_list = [file_path]
    	show_image()
        
def show_image():
	global image_list
	global current_id
	global photo
	global img
	img = Image.open(image_list[current_id])
	load_annotation()
	load_classification()
	resized_img = img.resize((800,800),resample=0)
	photo = ImageTk.PhotoImage(resized_img)
	Label(root, image=photo,width=800,height =800).grid(row=0, column=0,rowspan = 20,columnspan=2,sticky=W+E+N+S)


def load_annotation():
	global bbox
	bbox = []
	draw = ImageDraw.Draw(img)
	image_name = image_list[current_id].split('\\')[-1]
	detection_dir = image_list[current_id].replace(image_name,'').replace('image\\','detection-results\\')
	print (detection_dir+image_name.replace('.JPG','.txt'))
	with open(detection_dir+image_name.replace('.JPG','.txt'),'r') as f:
		detection_data = f.readlines()
	for data in detection_data:
		box = [int(i) for i in data.split(' ')[2:]]
		bbox.append(box)
		draw.rectangle((box[0],box[1],box[2],box[3]),outline='red',width = 5)
def load_classification():
	image_name = image_list[current_id].split('\\')[-1]
	refined_dir = image_list[current_id].replace(image_name,'').replace('image\\','refinment_results\\')
	if path.exists(refined_dir+image_name.replace('.JPG','.txt')):
		draw = ImageDraw.Draw(img)
		with open(refined_dir+image_name.replace('.JPG','.txt'),'r') as f:
			classification_data = f.readlines()
		for data in classification_data:
			box = [int(i) for i in data.split(' ')[2:]]
			draw.rectangle((box[0],box[1],box[2],box[3]),outline='yellow',width = 5)
		
def hightLight_box(box):
	global photo
	global img
	image = img.copy()
	draw = ImageDraw.Draw(image)
	draw.rectangle((box[0],box[1],box[2],box[3]),outline='green',width = 5)
	resized_img = image.resize((800,800),resample=0)
	photo = ImageTk.PhotoImage(resized_img)
	Label(root, image=photo,width=800,height =800).grid(row=0, column=0,rowspan = 20,columnspan=2,sticky=W+E+N+S)
def start_bird_box():
	global bbox,bird_index
	global img,box_img
	if (len(bbox)==0):
		return
	box = bbox[bird_index]
	nneg = lambda x: max(x,0)
	box_img = img.crop((nneg(box[0]-10),nneg(box[1]-10),(box[2]+10),(box[3]+10)))
	print (bird_index,len(bbox))
	show_bird()
	hightLight_box(box)
def next_bird_box():

	global bbox,bird_index
	global img,box_img
	bird_index +=1
	if (len(bbox)==0):
		return
	if (bird_index >= len(bbox)):
		return
	box = bbox[bird_index]
	nneg = lambda x: max(x,0)
	box_img = img.crop((nneg(box[0]-10),nneg(box[1]-10),(box[2]+10),(box[3]+10)))
	print (bird_index,len(bbox))
	show_bird()
	hightLight_box(box)
def show_bird():
	global photo2
	resized_img = box_img.resize((200,200),resample=0)
	photo2 = ImageTk.PhotoImage(resized_img)
	Label(root, image=photo2,width=200,height =200).grid(row=0, column=3,rowspan = 5,columnspan=1,sticky=W+E+N+S)

def create_classification(label = None, correct = True):
	global bird_index,bbox
	if (bird_index==len(bbox)):
		save_annotation()
		return
	if (correct==False):
		label =-1
	if (len(bbox[bird_index])==4):
		bbox[bird_index].append(label)
	else:
		bbox[bird_index][4] = label
	print (bbox[bird_index])
	next_bird_box()
def save_annotation():
	global bbox
	image_name = image_list[current_id].split('\\')[-1]
	refined_dir = image_list[current_id].replace(image_name,'').replace('image\\','refinment_results\\')
	print (refined_dir)
	if not os.path.exists(refined_dir):
		os.makedirs(refined_dir)
	with open(refined_dir+image_name.replace('.JPG','.txt'),'w') as f:
		print (bbox)
		for box in bbox:
			print ('listed,',box,len(bbox))
			f.writelines('bird {} {} {} {} {}\n'.format(box[4],box[0],box[1],box[2],box[3]))

def next_image():
	global current_id,bird_index
	global image_list
	bird_index = 0
	current_id+=1
	if(current_id>=len(image_list)):
		current_id-=1
	show_image()

def about():  
    print('Developed by Robert Ver1.0')   
if __name__ == '__main__':
	menubar = Menu(root)  
	photo = ImageTk.PhotoImage(img)
	Label(root, image=photo,width=800,height =800).grid(row=0, column=0,rowspan = 20,columnspan=2,sticky=W+E+N+S)
	#创建下拉菜单File，然后将其加入到顶级的菜单栏中  
	filemenu = Menu(menubar,tearoff=0)  
	filemenu.add_command(label="Open", command=open_file)
	filemenu.add_command(label="open_dir",command = open_folder)  
	filemenu.add_separator()  
	filemenu.add_command(label="Exit", command=root.quit)  
	menubar.add_cascade(label="File", menu=filemenu)  


	#创建下拉菜单Help  
	helpmenu = Menu(menubar, tearoff=0)  
	helpmenu.add_command(label="About", command=about)  
	menubar.add_cascade(label="Help", menu=helpmenu)  
	#显示菜单  
	root.config(menu=menubar)
	'''
	for idx,i in enumerate(specis_list):
		Button(root,width=20,height=2,text = i, command = lambda: save_annotation(correct = True,label = i)).grid(row = idx, column = 3,columnspan=1)
		['Mallard','Pintail','Green-winged teal','Gadwall','Shoveler','Widgeon','Canada Goose','Greater White-fronted Goose','Snow Goose']
	'''
	Button(root,width=20,height=2,text = 'Mallard', command = lambda: create_classification(correct = True,label = 'Mallard')).grid(row = 0, column = 4,columnspan=1)
	Button(root,width=20,height=2,text = 'Pintail', command = lambda: create_classification(correct = True,label = 'Pintail')).grid(row = 1, column = 4,columnspan=1)
	Button(root,width=20,height=2,text = 'Green-winged teal', command = lambda: create_classification(correct = True,label = 'Green-winged_teal')).grid(row = 2, column = 4,columnspan=1)
	Button(root,width=20,height=2,text = 'Gadwall', command = lambda: create_classification(correct = True,label = 'Gadwall')).grid(row = 3, column = 4,columnspan=1)
	Button(root,width=20,height=2,text = 'Shoveler', command = lambda: create_classification(correct = True,label = 'Shoveler')).grid(row = 4, column = 4,columnspan=1)
	Button(root,width=20,height=2,text = 'Widgeon', command = lambda: create_classification(correct = True,label = 'Widgeon')).grid(row = 5, column = 4,columnspan=1)
	Button(root,width=20,height=2,text = 'Canada Goose', command = lambda: create_classification(correct = True,label = 'Canada_Goose')).grid(row = 6, column = 4,columnspan=1)
	Button(root,width=20,height=2,text = 'Greater White-fronted Goose', command = lambda: create_classification(correct = True,label = 'Greater_White-fronted_Goose')).grid(row = 7, column = 4,columnspan=1)
	Button(root,width=20,height=2,text = 'Snow Goose', command = lambda: create_classification(correct = True,label = 'Snow_Goose')).grid(row = 8, column = 4,columnspan=1)
	
	Button(root,width=20,height=4,text = "wrong_anno",command = lambda: create_classification(correct = False),fg='red').grid(row = 5, column = 3)
	Button(root,width=20,height=4,text = "unknown",command = lambda: create_classification(correct = True,label = 'Not_Sure'),fg='red').grid(row = 6, column = 3)
	Button(root,width=20,height=4,text = "incorrect_box",command = lambda: create_classification(correct = True,label = 'incorrect_box'),fg='red').grid(row = 7, column = 3)
	Button(root,width=20,height=4,text = "inaccurate_box",command = lambda: create_classification(correct = True,label = 'inaccurate_box'),fg='red').grid(row = 8, column = 3)
	
	other_specis =tkinter.Entry(root,width=20)
	other_specis.grid(row = 9, column = 3)
	other_specis.focus_set()
	Button(root,width=20,height=4,text = "other",command = lambda: create_classification(correct = True,label =other_specis.get()),fg='red').grid(row = 9, column = 4)



	end_of_species = len(specis_list)
	#Button(root,width=20,height=4,text = "Start Annotation",command = start_bird_box,fg='black').grid(row = end_of_species, column = 3)
	Button(root,width=20,height=4,text = "Next_image",command = next_image,fg='green').grid(row = end_of_species+3, column = 3)
	mainloop()  