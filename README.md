# SpeciesLabelTool
This is a simple GUI for species labeling, aiming at provide a fast labeling tool for species labeling based on existing detection results/gt labels.

## Authors
Zhicheng(Robert) Tang

## Requirements 
```
pip install tk
pip install opencv-contrib-python
pip install glob
pip install Pillow==6.2.2 #6.1 also works
````

## Usage
Below shows the UI interface.


```
Section 1: shows the options to load image/annotation/config file
Section 2: Available categories for the label process
Section 3: An zoomed illustration of the current instance
Section 4: Whether to enable the custom func: Filter_class.
Section 5: Information shown current instance class name
Section 6: Utility functions to move forward/backward across instances/images.
```
### Load images (required)
Under the menubar Section 1, button 'Open', user can select 'open_image_dir', this will allows user to select the folder directory that contains image data. Once the target image dir is selected, the GUI will prompt with the first image available.

### Load labels/detections (Pick one)
There are two ways of loading the labels.

One is to load labels from groundtruth which only provide location information.('open_label_dir')

Another way is to load model detection & classification results provided by the ML models. Loading these file will provide with the location information as well as the class name of each individuals. These was predicted by the models developed by our team, so there might be some errors needed to be corrected. The predicted class name is shown in section 5. If its shows 'bird', then means the instance is not labeled.

**Attention**: If result file exists a corresponding result file, both process describe above will not be loaded (however user still have to choose one of them). Instead, the file under result file will be automatically used to resume previous result. To avoid that, simply delete the result file or change the output directory in the config file.

### Load customized configuration(optional)
A customized configuration can be loaded for extra function usage. Currently supported actions are: **Filter class**

Filter class enables the program to skip some predefined classes during the label process, a sample is provided under file custom_settings.json. See the example below: it means the program will skip the instance of 'Mallard' if the confidence score over 0.9 and 'Mallard Male' if the score is over 0.5. User can config these values in this json file and loaded them with the option of 'load_custom_settings' in Section 1.

```
{
    "filtered_class": {
        "Mallard": 0.9,
        "Mallard Male":0.5
    }
}
```

### Extra modification
Some extra modification can be made based on the needed of the labeling process. User can add/delete extra categories or change the output directory if needed, these can be found in the file bird_label_config.json. And will be automatically loaded every time the program runs.

### Labeling process
Step1:

Open the GUI tool by type command in the command window:
```
python GUI.py
```
Then finish the three sections described before:

    Load images, 
    Load labels/detections, 
    (Load customized configuration)

The program will show the images and bounding boxes in the large image view with the current labeling box in the smaller image view. Note that all the boxes are showing in blur color except the current focused one is in yellow.

***extra step***

If user choose to skip some specific class defined in the custom_settings.json, please check the box in section 4 to enable the filter process. Note if the custom_settings is not loaded ahead, the filter class wont work.


Step2:

Assign the current instance with a class name, the class name options are available on the right side in section 2, after click one of the class name, the program will jump to the next instance available. If the next instance doesn't change, it means arriving the end of all the available instance of this image. Every single operation in this section will trigger autosave for the current image result.


Step3:

After finish labeling all the instance of current image, click next_image/prev_image located in section 6, user can also skip/roll back instance by clicking Next_Bird/Prev_Bird. Every single operation in this section will trigger autosave for the current image result. These steps wont trigger auto save, and will not update results.

## Results format
The result will be generated as follows, under the directory defined in configs json file "out_dir". The file structure will be like:
```
Under 'out_dir'
Input_image_folder name
├── result_labels
│   ├── image_name1.txt
│   ├── image_name2.txt
│   ├── image_name3.txt
│   └── ...
```
For each result txt file, each instance is consists the following parts:
```
'class name','confidence score',box[0],box[1],box[2],box[3]'
Gadwall,0.9883061051368713,3325,1037,3403,1179
```
