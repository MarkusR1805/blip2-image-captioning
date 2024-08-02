<div align="center">
<h1> Blip2-Image-Captioning</h1>
</div>
<div><h2>For Mac (M1, M2, M3) Cuda (Windows/Linux), or CPU</h2> </div>
<div align="center">
  <p>
    <a href="#supported-formats">Supported Formats</a> •
    <a href="#installation">Installation</a> •
    <a href="#usage">Usage</a>
  </p>
</div>

![Picture1](https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/165788c5-17cf-4fa1-a6f3-b900a3a4e1ab/width=1440,quality=90/2024-05-21-201140_0_NIK.jpeg)
<p>
<div align="center">MR-XOTOX-NASSE-WAENDE-SDXL (https://civitai.com/models/448483?modelVersionId=499427)</div>
</p>

## Supported Formats
JPG, JPEG, PNG, BMP, GIF

## Installation

### Create a virtual Python environment in the same directory!
Open the terminal in the directory, e.g. /path/captioning/Blip2-Image-Captioning
```
python3.12 -m venv env
```
```
python env/bin/activate
```
### Install requirements.txt
```
pip install --upgrade pip
```
```
pip install -r requirements.txt
```
or
```
pip install huggingface-hub
pip install language-tool-python
pip install language_data
pip install nltk
pip install pillow
pip install psutil
pip install sentencepiece
pip install tokenizers
pip install torch
pip install torchaudio
pip install torchsde
pip install torchvision
pip install transformers
```
![Picture2](https://creative-ai.der-zerfleischer.de/images/creativ/quer//2024-05-17-103401_109585519072628_barock.jpeg)
## Use Model
Start the programm in terminal with
```
python main.py
```

### Salesforce [blip2-opt-2.7b](https://huggingface.co/Salesforce/blip2-opt-2.7b) with ≈ 3.744.679.936 params
Approximately 15 GB in size. Either you use the programme as it is set (from Huggingface), or you load the model locally on your computer and have to change the path to "main.py".
You must then adapt these lines of code!<p>
#model_path = "/Volumes/SSD T7/Salesforce-blip2-opt-27b" # Local path<p>
or
model_path = "Salesforce/blip2-opt-2.7b" # Huggingface path<p>

## Usage
<h2>Attention! All text files in the directory will be deleted without being asked! All files with the suffix .txt!!!</h2>

You must be in the programme directory in the terminal, then start the programme with "python main.py"

### This application is used via the terminal, here I show it using the example of a MacBook M3

First question: The path to the directory in which the images are located
Second question: The path to ignore_list.txt (leave empty if no explicit file exists) Default is the programme path
Third question: The path to allowed_list.txt (leave empty if no explicit file exists) Default is the programme path
Fourth question: Additional keywords 2-3 or more at the very beginning of the image description (enter separated by a comma)

The programme creates text files with the same name as the image, example image1.png = image1.txt
First, only image descriptions are created for all images, then keywords are filtered from the image description and placed in front of the image description in addition to the keywords you entered at the beginning.
The following files are also created:
1. gesamt.txt / All image descriptions in one file, ideal for use as a wildcard
2. extracted_words.txt / all keywords of all images can be found here
3. t_extracted_words.txt / as in 2 but with the tokens added
4. a CSV table with image description and image path

![Picture3](https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/fe8c5bfd-7887-4267-a344-a18189a41680/width=920,quality=90/2024-06-06-143307_305791123400292.jpeg)

## You can adapt and change the python code and also change the parameters of the model. Just experiment with the changes, you can also use the larger Blip2 model but it has 33GB and takes longer to process the images.
## [Salesforce](Salesforce/blip2-opt-6.7b) or little better [Salesforce-Coco](Salesforce/blip2-opt-6.7b-coco)
