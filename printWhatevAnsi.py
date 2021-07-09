#!/usr/bin/python3

from PIL import Image
import math, sys
figure=" "
regular=" "
em = " "
en = " "
scale=[
	"\x1b[30m",
	"\x1b[3{}m",
	"\x1b[9{}m"

]
def hue_raw(fullpixel):
	global threshhold_global
	hue_arr = [False,False,False]
	if (fullpixel[0] >=threshhold_global ):
		hue_arr[0] = True
	if (fullpixel[1] >=  threshhold_global):
		hue_arr[1] = True
	if (fullpixel[2] >=  threshhold_global ):
		hue_arr[2] = True
	return hue_arr
def hue(fullpixel):
	global threshhold_global
	hue_arr=hue_raw(fullpixel)
	return hue_arr[0]*1+hue_arr[1]*2+hue_arr[2]*4

def weighted_average(fullpixel):
	global threshhold_global
	hue_arr=hue_raw(fullpixel)
	count=0
	pixsum=0
	for i in range(3):
		if (hue_arr[i]):
			count+=1
			pixsum+=fullpixel[i]
	if count==0:
		count=3
	return pixsum//count
threshhold_global=127
def image_2_whatev_ansi(filename, char="⬤", output="", dither=True, double_flag = False):
	global threshhold_global
	if double_flag:
		pixelWidth=2
	else:
		pixelWidth=1
	image = Image.open(filename).convert("RGB")
	imgdump = image.load()
	if output != "":
		output_file = open(output,"wb")
	for y in range(image.height):
		string = "\x1b[40m"
		for x in range(image.width):
			pixel = imgdump[x,y]
			for i in range(3):
				if (pixel[i] > 256):
					pixel[i] = 256
            
			hue_arr=hue_raw(pixel)
			color=hue(pixel)
			brightness=weighted_average(pixel) // 85
			if (brightness>2):
				brightness=2
			string += (scale[brightness].format(color)+char) * pixelWidth
			if dither:
				new_pixel=[].extend(pixel)
				pixels_i_care_about=[None,None,None,None]
				if x!=image.width-1:
					pixels_i_care_about[0]=[].extend(imgdump[x+1,y])
				if y!=image.height-1 and x!=image.width-1:
					pixels_i_care_about[1]=[].extend(imgdump[x+1,y+1])
				if y!=image.height-1:
					pixels_i_care_about[2]=[].extend(imgdump[x,y+1])
				if x!=0 and y!=image.height-1:
					pixels_i_care_about[3]=[].extend(imgdump[x-1,y+1])
				for i in range(3):
					if (hue_arr[i]):
						error=pixel[i]%85
					else:
						error=0
					
					
					if pixels_i_care_about[0]!=None:
						pixels_i_care_about[0][i] += math.floor((7/16)*error)
					if pixels_i_care_about[1]!=None:
						pixels_i_care_about[1][i] += math.floor((1/16)*error)
					if pixels_i_care_about[2]!=None:
						pixels_i_care_about[2][i] += math.floor((5/16)*error)
					if pixels_i_care_about[3]!=None:
						pixels_i_care_about[3][i] += math.floor((3/16)*error)
				if pixels_i_care_about[0]!=None:
					imgdump[x+1,y] = tuple(pixels_i_care_about[0])
				if pixels_i_care_about[1]!=None:
					imgdump[x+1,y+1] = tuple(pixels_i_care_about[1])
				if pixels_i_care_about[2]!=None:
					imgdump[x,y+1] = tuple(pixels_i_care_about[2])
				if pixels_i_care_about[3]!=None:
					imgdump[x-1,y+1] = tuple(pixels_i_care_about[3])
		if output == "":
			print(string)
		else:
			output_file.write(string.encode('utf_8'))
			output_file.write(bytes([13,10]))
	if output != "":
		output_file.close()

help_text="""
Usage: printWhatevAnsi.py image [-h] [-d [-i] [-w] [-t #n] [-c char]
	
	-h: Print this
	-d: Disable Dithering
    -w: print every character twice
	-t: use threshhold for hue selection
	-c: set which character to print
"""
if __name__ == "__main__":
	argc=len(sys.argv)
	if (argc==1):
		print ("NO")
		sys.exit(1)
	in_file=sys.argv[1]
	dither_flag=True
	pixel_width_flag=False
	scale_select=0
	custom_char="⬤"
	while (argc>2 and sys.argv[2][0]=="-"):
		if sys.argv[2]=="-h":
			print(help_text)
			sys.exit(0)
		elif sys.argv[2]=="-d":
			dither_flag=False
		elif sys.argv[2]=="-w":
			
			pixel_width_flag=True
		elif sys.argv[2]=="-t":
			if argc>3 and sys.argv[3].isnumeric() and int(sys.argv[3])>=0:
				threshhold_global=int(sys.argv[3])
				for i in range(3,len(sys.argv)-1):
					sys.argv[i]=sys.argv[i+1]
				argc=argc-1
		elif sys.argv[2]=="-c":
			custom_char=sys.argv[3][0]
			for i in range(3,len(sys.argv)-1):
				sys.argv[i]=sys.argv[i+1]
			argc=argc-1				
		for i in range(2,len(sys.argv)-1):
			sys.argv[i]=sys.argv[i+1]
		argc=argc-1
			
		
	if (argc>2):
		out_file=sys.argv[2]
	else:
		out_file=""
	image_2_whatev_ansi(in_file, output="", dither=dither_flag, double_flag = pixel_width_flag,char=custom_char)
