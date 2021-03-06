#!/usr/bin/python3

from PIL import Image
import math, sys
figure=" "
regular=" "
em = " "
en = " "
scale = ["█" ,"▓","▒", "░", " "]
def image_2_block(filename, output="", dither=True, inverse = False, double_flag = False, space = ""):
	if double_flag:
		pixelWidth=2
	else:
		pixelWidth=1
	if space != "":
		scale[4] = space
	image = Image.open(filename).convert("L")
	imgdump = image.load()
	if output != "":
		output_file = open(output,"wb")
	for y in range(image.height):
		string = ""
		#output_file.write(bytes([9]))
		for x in range(image.width):
			pixel = imgdump[x,y]

			if (pixel > 256):
				pixel = 256
			if (inverse):
				string += scale[4-(pixel // 52)] * pixelWidth
			else:
				string += scale[pixel // 52] * pixelWidth
			if dither:
				error=pixel%52
				if x!=image.width-1:
					imgdump[x+1,y] += math.floor((7/16)*error)
				if y!=image.height-1 and x!=image.width-1:
					imgdump[x+1,y+1] += math.floor((1/16)*error)
				if y!=image.height-1:
					imgdump[x,y+1] += math.floor((5/16)*error)
				if x!=0 and y!=image.height-1:
					imgdump[x-1,y+1] += math.floor((3/16)*error)
		if output == "":
			print(string)
		else:
			output_file.write(string.encode('utf_8'))
			output_file.write(bytes([13,10]))
	if output != "":
		output_file.close()

help_text="""
Usage: printBlock.py image [-h] [-d] [-i] [-w]
	
	-h: Print this
	-d: Disable Dithering
	-w: print every character twice
	-i: invert
"""
if __name__ == "__main__":
	argc=len(sys.argv)
	if (argc==1):
		print ("NO")
		sys.exit(1)
	in_file=sys.argv[1]
	dither_flag=True
	invert_flag=False
	pixel_width_flag=False
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
		for i in range(2,len(sys.argv)-1):
			sys.argv[i]=sys.argv[i+1]
		argc=argc-1
			
		
	if (argc>2):
		out_file=sys.argv[2]
	else:
		out_file=""
	image_2_block(in_file, output="", dither=dither_flag, inverse=invert_flag, double_flag = pixel_width_flag)
