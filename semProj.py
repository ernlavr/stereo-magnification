from os import walk
import os
from pathlib import Path
import cv2
import subprocess
import re
import shutil

skipImgs = 2

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def makedir(dir):
    Path("dir").mkdir(parents=True, exist_ok=True)

def clearOutputDir(idx):
    if(os.path.exists(rawOutput[idx])):
        import shutil
        shutil.rmtree(rawOutput[idx])
    os.mkdir(rawOutput[idx])

folders = ["examples/column/", "examples/corridor/", "examples/garden/", "examples/plant/", "examples/starbucks/"]
imgFolder = [i + "input/" for i in folders]
rawOutput = [i + "rawOutput/" for i in folders]
renderingsFolder = [i + "renderings/" for i in folders]
for i, item in enumerate(folders):
    imgs = []
    renderMultiple = 4
    clearOutputDir(i)
    for (dirpath, dirnames, filenames) in walk(imgFolder[i]):
        imgs = filenames

    imgs.sort(key=natural_keys)

    for index in range(len(imgs) - 2):
        # Prepare commands
        image1 = imgFolder[i] + imgs[index]
        image2 = imgFolder[i] + imgs[index + 2]
        output_dir = rawOutput[i] + imgs[index]
        makedir(output_dir)
        subprocess.call(['python', 'mpi_from_images.py', f"--image1={image1}", f"--image2={image2}", f"--output_dir={output_dir}", "--fx=0.775793", "--fy=1.034418", "--xoffset=0.0082", "--min_depth=0.1", f"--render_multiples={renderMultiple}", "--render"])
        rendering = f"render_00_{renderMultiple}.0.png"
        renderingPath = output_dir + "/" + rendering
        if os.path.exists(renderingsFolder[i]) is False:
            os.mkdir(renderingsFolder[i])
        shutil.copyfile(renderingPath, renderingsFolder[i] + f"rend_{renderMultiple}_{imgs[index]}")
        print(f"Done {index} / {len(imgs)}")




#--image1=examples/twain/twain_left.jpg \ --image2=examples/twain/twain_right.jpg \ --output_dir=examples/twain/results \ --fx=1.722207943 \ --fy=2.296277257 \ --xoffset 0.0082 \ --render_multiples 2 3 \ --render