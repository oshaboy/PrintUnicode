#!/usr/bin/python3

from PIL import Image
import math, sys
figure=" "
regular=" "
em = " "
en = " "

def distribute_error(imgdump, x, y, w, h):
	global threshhold_global
	pixel = imgdump[x,y]
	error=pixel-threshhold_global*(pixel>=threshhold_global)
	if x!=w-1:
		imgdump[x+1,y] += math.floor((7/16)*error)
	if y!=h-1 and x!=w-1:
		imgdump[x+1,y+1] += math.floor((1/16)*error)
	if y!=h-1:
		imgdump[x,y+1] += math.floor((5/16)*error)
	if x!=0 and y!=h-1:
		imgdump[x-1,y+1] += math.floor((3/16)*error)
	return error
def image_2_whatev(filename, char="⬤", output="", dither=True, inverse = False, double_flag = False, space = " "):
	global threshhold_global
	if double_flag:
		pixelWidth=2
	else:
		pixelWidth=1
	image = Image.open(filename).convert("L")

	imgdump = image.load()
	if output != "":
		output_file = open(output,"wb")
	for y in range(image.height):
		string = ""
		#output_file.write(bytes([9]))
		for x in range(image.width):
			pixel = imgdump[x,y]
			if ((pixel>=threshhold_global) ^ inverse):
				string+=char*pixelWidth
			else:
				string+=space*pixelWidth
			if dither:
				distribute_error(imgdump,x,y, image.width, image.height)
		if output == "":
			print(string)
		else:
			output_file.write(string.encode('utf_8'))
			output_file.write(bytes([13,10]))
	if output != "":
		output_file.close()

help_text="""
Usage: printWhatev.py image [-h] [-d] [-t #n] [-i] [-w] [-c char]
	
	-h: Print this
	-d: Disable Dithering
	-t: Set threshhold value
	-i: invert
	-w: print every character twice
	-c: set which character to print
"""
if __name__ == "__main__":
	global threshhold_global
	threshhold_global=128
	argc=len(sys.argv)
	if (argc==1):
		print ("NO")
		sys.exit(1)
	in_file=sys.argv[1]
	dither_flag=True
	invert_flag=False
	pixel_width_flag=False
	custom_char="⬤"
	while (argc>2 and sys.argv[2][0]=="-"):
		if sys.argv[2]=="-h":
			print(help_text)
			sys.exit(0)
		elif sys.argv[2]=="-d":
			dither_flag=False

		elif sys.argv[2]=="-w":
			
			pixel_width_flag=True
		elif sys.argv[2]=="-i":
			invert_flag=True
		elif sys.argv[2]=="-c":
			custom_char=sys.argv[3][0]
			for i in range(3,len(sys.argv)-1):
				sys.argv[i]=sys.argv[i+1]
			argc=argc-1
		elif sys.argv[2]=="-t":
			if argc>3 and sys.argv[3].isnumeric() and int(sys.argv[3])>=0:
				threshhold_global=int(sys.argv[3])
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
	image_2_whatev(in_file,char=custom_char, output="", dither=dither_flag, inverse=invert_flag, double_flag = pixel_width_flag)
