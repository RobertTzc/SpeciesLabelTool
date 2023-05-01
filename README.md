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
## Load images (required)
1. In the top left under "Open" in section 1, select 'open_image_dir'. This will bring up a window to navigate to and select the folder directory that contains the images to correct labels. Once the target image dir is selected, the GUI will display the first image (alphabetically) in the folder directory.

## Load labels or detections (Pick one)
There are two ways of loading the detection and classification labels associated with the labeled images.

1. open_label_dir -> loads labels with only location information - use for automated labels that do not provide species classification information
2. open_detection_dir -> loads labels from models with species classification results - use for automated labels that provide species classification information

## Customization Options (Optional)

1. Add/Delete species categories buttons for labeling
The user is able to define their own list of classes to label the birds as using the bird_label_config.json file. A sample is provided under the file "bird_label_config.json" and is also outlined below. In the example file, the program will give the user the options to label birds as Mallard, Pintail, and Shoveler. Notice that the final category does not contain a comma after the ".

```
    "classList": [
        "Mallard",
        "Pintail",
        "Shovelor"
    ],
```

To edit this configuration file in Windows, open the bird_label_config.json file in notepad and add or remove categories. For example, in the below example we add sex options to each of the categories. You may add as many or as few categories for labeling as you would like.

```
{
    "classList": [
        "Mallard_Male",
        "Mallard_Female",
        "Pintail_Male",
        "Pintail_Female",
        "Shovelor_Male",
        "Shovelor_Female"
    ],
}
```

2. Change the output directory to save results
Instructions Coming Soon!

3. Filter automated labels to only show specific classes
Filter class enables the program to skip some predefined classes during the labeling process to try and speed up the labeling process. A sample is provided under the file "custom_settings.json" and is also outlined below. In the example file, the program will skip the instance of 'Mallard' if the confidence score over 0.9 and 'Mallard Male' if the score is over 0.5. 

```
{
    "filtered_class": {
        "Mallard": 0.9,
        "Mallard Male":0.5
    }
}
```

To edit this configuration file in Windows, open the custom_settings.json file in notepad and add or remove categories and confidence scores. For example, in the below example we add the program to skip Gadwall if the score is over 0.75 and remove the skipping of Mallard Male over 0.5. You may add as many or as few categories to skip as you would like.

```
{
    "filtered_class": {
        "Mallard": 0.9,
        "Gadwall":0.75
    }
}
```

## Loading Customization Options
The list of species classification buttons and output directly will be automatically loaded. 

To load the filtered species to not see, in the top left under "Open" in section 1, select 'load_custom_settings'. This will bring up a window to navigate to and select the file that contains the custom settings, the custom_settings.json file. Select the custom_settings.json file and click open. Next, on the main screen under section 4, select the empty box next to "filter class". This will activate the filter categories and remove them so they will be skipped over by the tool.

## Labeling Birds
The main window of the program will show the current image and all bird bounding boxes (blue boxes) in the large image view. The current bird to be labeled will be shown in the smaller image view in the upper right, and the bounding box of this bird will change to yellow in the large image view to highlight the current bird.

To assign the currently selected bird (the one shown in the top right with a yellow bounding box), simply select the species classification name from the menu on the right side of the screen in Section 2. Once one is selected, the program will jump to the next instance available. If you want to skip the bird and not reclassify it, click the green "Next_Bird" button. If you accidentally mis-label or skip a bird, use the Prev_Bird button to go back to the previous bird. If after selecting a species class or selecting "Next_Bird" and the program doesn't bring up a new bird, it means you have gone through all the birds in that image. Select the blue "Next_Image" button to go to the next image. Anytime you select a species classification, the label file gets automatically updated and the new version is saved. 

## Results and Output
The result will be generated as follows, under the directory defined in configs json file "out_dir". The base directory is within the SpeciesLabelTool-main folder under a new folder with the same name as the folder containing the images.

The file structure will be like:
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
Example:
Gadwall,0.9883061051368713,3325,1037,3403,1179
```
