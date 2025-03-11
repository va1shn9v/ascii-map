# ASCII MAP GENERATOR

## Approach:
The Overall Approach is based on the following steps:

**Data** &rarr; **Mercator Projection + Inverting** &rarr; **Generating Plot Image + Grayscale Conversion** &rarr; **Image to Ascii Conversion**

### Data
The data contained the postal code and lattitude and longitude coordinates of each postal code:

![alt text](image.png)

While looking at the data csv, some descripencies were found, where the values of the lattitude exceeded the actual range of (-90,90), hence these rows were eliminated.
![alt text](bad_data.png)

Initially, to have a look at the data, I made a scatter plot of the data with latitude as y coordinate and longitude as the x coordinate.

![alt text](vanilla_scatter.png)

As seen in the above image, the plot does not bear any resemblance to the UK map.

### Mercator Projection

Therefore inorder to adjust the coordinates, we need to project them onto a 2D surface. I used the mercater projection to convert the latitudes and longitudes to x,y coordinates for plotting.
- Ref: https://en.wikipedia.org/wiki/Mercator_projection
- Ref: https://stackoverflow.com/questions/14329691/convert-latitude-longitude-point-to-a-pixels-x-y-on-mercator-projection


Post applying the mercator projection and flipping the image to have higher latitudes in the start:
![alt text](scatter_plot.png)

Caveat: Aspect Ratios, have been manually fixed, dynamic calculation based on the range of latitudes did not yeild good results.
In the above plot, all the axis were dropped from the plot, to facilitate image generation of this plot.

### Image Generation and Grayscale Conversion
The axis are removed and the plot is saved to an image, this essentially allows to dicretize the plot to integer x,y coordinates(pixel locations), which would ennable us to place the ascii text for generation.

The Grayscale image:
![alt text](grayscale_img.png)

### Image to ASCII conversion
Resize the imge to account for the character size(the value is empiracal, found this was needed, when comparing my results with the ones generated from online tools).
Then After thresholding the Grayscale values based on the number of different characters we would like to use, we can loop over the image and write the ASCII art string.

- Ref: https://github.com/kiteco/python-youtube-code/tree/master/ascii

![alt text](result.png)

### Results:

To run the file use
```
uv run ascii_art.py
```

This file supports the following arguments:

```
--chars : List of ascii characters to use, all the characters to be used are supposed to passed as a comma seperated list
--file_path: Path to the CSV file to load data
--sea: Setting this value to True, will use "." character for all the sea locations/pixels in the art.
```

Sample results:

```
uv run ascii_art.py
```
<img width="404" alt="image" src="https://github.com/user-attachments/assets/5f694d1e-55fb-434f-aa42-17037a0df540" />

```
uv run ascii_art.py --sea
```
<img width="359" alt="image" src="https://github.com/user-attachments/assets/323c0dad-f0fe-4947-8af5-b2ca033aa172" />




```
uv run ascii_art.py --sea --chars @,a,b,c,d
```
<img width="371" alt="image" src="https://github.com/user-attachments/assets/02a1eea7-9fc1-491c-b360-9eaf167e613c" />

### Installation
Inorder to install the required packages  you can choose to install and run `uv`:
First install uv :
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```
and then run 

```
uv sync
```
or

```
uv add pandas matplotlib numpy
```

Alternatively, they could be installed using `pip install pandas matplotlib numpy`





