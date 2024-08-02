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
![Picture2](https://creative-ai.der-zerfleischer.de/images/creativ/quer//2024-05-17-103401_109585519072628_barock.jpeg)
## Use Model

### Salesforce [blip2-opt-2.7b](https://huggingface.co/Salesforce/blip2-opt-2.7b) with ≈ 3.744.679.936 params
Approximately 15 GB in size. Either you use the programme as it is set (from Huggingface), or you load the model locally on your computer and have to change the path to "main.py".
You must then adapt these lines of code!<p>
model_path = "/Volumes/SSD T7/Salesforce-blip2-opt-27b" # Local path<p>
#model_path = "Salesforce/blip2-opt-2.7b" # Huggingface path<p>

## Usage

### This application is used via the terminal, here I show it using the example of a MacBook M3
![Picture3](https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/fe8c5bfd-7887-4267-a344-a18189a41680/width=920,quality=90/2024-06-06-143307_305791123400292.jpeg)
