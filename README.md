# SpeciesLabelTool

## About
This is a simple GUI for quick species labeling, to provide a fast labeling tool for species labeling based on labels created from automated detection and/or species classification. It is built to correct automated detections and classification to quickly increase the amount of training data available to improve classification results by automated algorithms.

## Authors
Zhicheng(Robert) Tang

## Software/Hardware Requirements
Anaconda: https://www.anaconda.com/ (will need system admin privileges)

Python: https://www.python.org/ (will need system admin privileges)

Windows 10
- Anaconda3
- Python 3.9

Other

# Installation and Set Up

## Opening Anaconda
To start Anaconda on Windows, you may either:
1. Use the Start Menu to Search for Anaconda Prompt and select Anaconda Prompt to open the command window for Anaconda
2. Navigate to the Anaconda Prompt icon [default location C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Anaconda3 (64-bit)] (or Anaconda Prompt shortcut icon) and double-click to run the command window for Anaconda

## Cloning the Repository from GitHub
To clone the repository from GitHub there are a two main options:
1. Download and unzip directly from GitHub (recommended)
* Navigate to the GitHub repository for the SpeciesLabelTool here: https://github.com/RobertTzc/SpeciesLabelTool
* In the upper right, click on the <>Code dropdown arrow and select Download ZIP
* After download, extract the SpeciesLabelTool-main.zip folder and move it to the desired location on your machine. Recommended is under C:\Users\\*yourusername*
* If you are successful with step 1, skip to Creation and Activation of Virtual Environment.

If needed, for additional help with this step, please refer to the link here: https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository

## Creation and Activation of Virtual Environment
Create your virtual environment in Anaconda Prompt. The following is a demo using Python 3.8 and Anaconda to create a virtual environment: *Note*: You may name the virtual environment whatever you choose. In our example, we use the name "species_label".

* Open Anaconda Prompt 

* Creating the virtual environment:
```
conda create -n species_label python==3.8
```
* Activating the virtual environment:
```
conda activate species_label
```
For more information on creating and activating virtual environments, see: https://conda.io/projects/conda/en/latest/user-guide/getting-started.html 

## Installation of Required Packages
### 1. Within a Virtual Environment
After creating and activating a virtual environment, we recommend installing packages within the virtual environment.

* To install the required packages, run the following code after creating and activating the virtual environment:
```
pip install tk
pip install opencv-contrib-python
pip install glob
pip install Pillow==6.2.2
````
*Note*: For installation of Pillow==6.2.2, 6.1 also works. Try using Pillow==6.1 if errors arise attempting to install Pillow==6.2.2

## Future Activation of the Virtual Environment

After creation of the Virtual Environment the first time, you do NOT need to re-create the virtual environment and re-install the packages each time you use Anaconda and wish to run the Waterfowl Detection and Classification Inference Interface.

* To activate the Virtual Environment in future sessions, simply run the following code after opening Anaconda Prompt.
```
conda activate species_label
```
*Note*: Keep in mind that the name of your virtual environment may be different than ours (user's choice). Our virtual environment is named: species_label

## Running the Interface
* Ensure you are in your virtual environment in Anaconda that you previously created for running the GUI in the above steps. In Anaconda prompt, you should see (*yourvirtualenvironment*) *YourDirectory*>

* If you see (base) *YourDirectory*>   , activate your virtual environment by running:
```
conda activate species_label
```
*Note*: Keep in mind that the name of your virtual environment may be different than ours (user's choice). Our virtual environment is named: species_label

* Once you are in your virtual environment, change your directory in Anaconda to the SpeciesLabelTool-main folder using the code: cd C:\Users\\*yourusername*\SpeciesLabelTool-main
```
cd C:\Users\yourusername\SpeciesLabelTool-main
```
* Next, run the GUI.py file to start the interface program:
```
python GUI.py
```
*Note*: If you receive an error referring to a missing module, ensure you are in the virtual environment created for running this interface and all packages were successfully installed in the above steps.

*Note*: If you receive an error "No file found GUI.py", ensure that you are in the correct directory and are under the SpeciesLabelTool-main folder in Anaconda prompt.

# GUI Usage
Below shows the GUI and demonstrates how to use it.

![Screenshot from 2023-03-12 23-16-00](https://user-images.githubusercontent.com/71574752/224606950-3f6a0e4a-187a-4996-9f45-384410fb1f9f.png)
```
Section 1: Menu for loading images, annotation files, and custom files
Section 2: Menu of species labeling selection buttons
Section 3: Enlarged image of the bird currently selected for labeling
Section 4: Selection to filter classes (species) to just those specified by the custom settings
Section 5: Current species classification (Updates if new class is selected from the menu in section 2)
Section 6: Utility functions to move forward/backward across birds/images
```
### Load images (required)
1. In the top left under "Open" in section 1, select 'open_image_dir'. This will bring up a window to navigate to and select the folder directory that contains the images to correct labels. Once the target image dir is selected, the GUI will display the first image (alphabetically) in the folder directory.

### Load labels or detections (Pick one)
There are two ways of loading the detection and classification labels associated with the labeled images.

1. open_label_dir -> loads labels with only location information - use for automated labels that do not provide species classification information or manual labels that contain species classification information made in LabelMe
2. open_detection_dir -> loads labels from model detection and species classification results provided by our models

**Attention**: If result file exists a corresponding result file, both process describe above will not be loaded (however user still have to choose one of them). Instead, the file under result file will be automatically used to resume previous result. To avoid that, simply delete the result file or change the output directory in the config file.

### Customization Options

1. Add/Delete species categories buttons for labeling

2. Change the output directory to save results

3. Filter automated labels to only show specific classes
Filter class enables the program to skip some predefined classes during the label process, a sample is provided under file custom_settings.json. See the example below: it means the program will skip the instance of 'Mallard' if the confidence score over 0.9 and 'Mallard Male' if the score is over 0.5. User can config these values in this json file and loaded them with the option of 'load_custom_settings' in Section 1.

```
{
    "filtered_class": {
        "Mallard": 0.9,
        "Mallard Male":0.5
    }
}
```

## Labeling Process
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
