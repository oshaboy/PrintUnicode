#!/usr/bin/python3

from PIL import Image
import math,sys	
all_sixels=[
" ","🬀","🬁","🬂","🬃","🬄","🬅","🬆","🬇","🬈","🬉","🬊","🬋","🬌","🬍","🬎"
,"🬏","🬐","🬑","🬒","🬓","🬔","▌","🬕","🬖","🬗","🬘","🬙","🬚","🬛","🬜","🬝",
"🬞","🬟","🬠","🬡","🬢","🬣","🬤","🬥","🬦","🬧","▐","🬨","🬩","🬪","🬫","🬬",
"🬭","🬮","🬯","🬰","🬱","🬲","🬳","🬴","🬵","🬶","🬷","🬸","🬹","🬺","🬻","█"
]
def threshhold_func(pix):
	global threshhold_global
	if pix>=threshhold_global:
		return 1
	return 0
def distribute_error(imgdump, x, y, w, h):
	global threshhold_global
	pixel = imgdump[x,y]
	error=pixel-threshhold_global*(pixel>=threshhold_global)
	if x!=w-1:
		imgdump[x+1,y] += math.floor((7/16)*error)
	if y!=h-1:
		imgdump[x,y+1] += math.floor((5/16)*error)
	if x!=0 and y!=h-1:
		imgdump[x-1,y+1] += math.floor((4/16)*error)
	return error
def image_2_braille(filename, output="", dither=True, inverse = False):
	image = Image.open(filename).convert("L")
	imgdump = image.load()
	if output != "":
		output_file = open(output,"wb")
	for y in range(0, image.height, 3):
		string = ""
		for x in range(0, image.width, 2):
			charnum = inverse * 64
			if imgdump[(x,y)] >= threshhold_global:
				charnum+=1 * ((not inverse) - (inverse))
			if dither:
				distribute_error(imgdump, x, y, image.width, image.height)
			if x+1 != image.width:
				if imgdump[(x+1,y)] >= threshhold_global:
					charnum+=2 * ((not inverse) - inverse)
				if dither:
					distribute_error(imgdump, x, y, image.width, image.height)
			if y+1 < image.height:
				if imgdump[(x,y+1)] >= threshhold_global:
					charnum+=4 * ((not inverse) - inverse)
				if dither:
					distribute_error(imgdump, x, y+1, image.width, image.height)
			if x+1 != image.width and y+1 < image.height:
				if imgdump[(x+1,y+1)] >= threshhold_global:
					charnum+=8 * ((not inverse) - inverse)
				if dither:
					distribute_error(imgdump, x+1, y+1, image.width, image.height)
			if y+2 < image.height:
				if imgdump[(x,y+2)] >= threshhold_global:
					charnum+=16 * ((not inverse) - inverse)
				if dither:
					distribute_error(imgdump, x, y+2, image.width, image.height)
			if x+1 != image.width and y+2 < image.height:
				if imgdump[(x+1,y+2)] >= threshhold_global:
					charnum+=32 * ((not inverse) - inverse)
				if dither:
					distribute_error(imgdump, x+1, y+2, image.width, image.height)
			string += all_sixels[charnum]

		if output == "":
			print(string)
		else:
			output_file.write(string.encode('utf_8'))
			output_file.write(bytes([13,10]))
	if output != "":
		output_file.close()
help_text="""
Usage: printBraille.py image [-h] [-d] [-t #n] [-i] [-6]
	
	-h: Print this
	-d: Disable Dithering
	-t: Set threshhold value
	-i: invert
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
	subset_flag=False
	while (argc>2 and sys.argv[2][0]=="-"):
		if sys.argv[2]=="-h":
			print(help_text)
			sys.exit(0)
		elif sys.argv[2]=="-d":
			dither_flag=False
		elif sys.argv[2]=="-t":
			if argc>3 and sys.argv[3].isnumeric() and int(sys.argv[3])>=0:
				threshhold_global=int(sys.argv[3])
				for i in range(3,len(sys.argv)-1):
					sys.argv[i]=sys.argv[i+1]
				argc=argc-1
		elif sys.argv[2]=="-i":
			invert_flag=True
		for i in range(2,len(sys.argv)-1):
			sys.argv[i]=sys.argv[i+1]
		argc=argc-1
			
		
	if (argc>2):
		out_file=sys.argv[2]
	else:
		out_file=""
	image_2_braille(in_file, output="", dither=dither_flag, inverse=invert_flag)
