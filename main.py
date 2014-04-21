from PIL import Image

im = Image.open("photo.jpg") #Enter photo name here
im.putalpha(0)
imdata = im.getdata()
letter_num = 0
lower_bound = 50 #at which value do things become black
output=""

def monochrome(im,v): #v is value: 0 = red, 1 = blue, 2 = green
	for x in range(im.size[0]):
		for y in range(im.size[1]):
			pixel=im.getpixel((x,y))
			value = pixel[v]
			im.putpixel((x,y),(value, value, value, 255))

def monotrans(im,l):
	for x in range(im.size[0]):
		for y in range(im.size[1]):
			pixel = im.getpixel((x,y))
			if(pixel[:3]>(l,l,l)):
				im.putpixel((x,y),(255,255,255,0))
			else:
				val = pixel[0]
				im.putpixel((x,y), (0,0,0,255-val))

def normalize(im, l): #l is lower bound for whiteness
	print("Normalizing image...")
	for x in range(im.size[0]):
		for y in range(im.size[1]):
			pixel = im.getpixel((x,y))
			if(pixel[:3]>(l,l,l)):
				im.putpixel((x,y),(255,255,255,0))
			else:
				im.putpixel((x,y), (0,0,0,255))
	im.save("normalized.png")
	print("Image normalized!")

def find_letter(im, starting_x, starting_y, lc):
	global letter_num
	blank = True #start x
	start_x = 0
	columnsum=0
	for x in range(starting_x, im.size[0]):
		if(columnsum!=0):
			start_x=x-1
			break
		columnsum=0
		for y in range(starting_y, im.size[1]):
			pixelr = im.getpixel((x,y))[0]
			columnsum+=255-pixelr
	end_x = 0 #end x
	blank = False
	columnsum=1
	for x in range(start_x, im.size[0]):
		if(columnsum==0):
			end_x=x-2
			break
		columnsum=0
		for y in range(starting_y, im.size[1]):
			pixelr = im.getpixel((x,y))[0]
			columnsum+=255-pixelr
	start_y = 0
	blank = True
	rowsum = 0
	for y in range(starting_y, im.size[1]):
		if(rowsum!=0):
			start_y=y-1
			break
		rowsum=0
		for x in range(start_x, end_x):
			pixelr = im.getpixel((x,y))[0]
			rowsum+=255-pixelr

	end_y = 0
	blank = True
	rowsum = 1
	for y in range(start_y, im.size[1]):
		if(rowsum==0):
			end_y=y-1
			break
		rowsum=0
		for x in range(start_x, end_x):
			pixelr = im.getpixel((x,y))[0]
			rowsum+=255-pixelr
	if(start_x!=0 and end_x!=0):
		letter_num+=1
		values = define_letter(im.crop((start_x, start_y, end_x,end_y)))
		if(lc.lower()=="l"):
			learn(values, input("Enter the {0} letter: ".format(letter_num)))
		elif(lc.lower()=="c"):
			check(values)
		elif(lc.lower()=="lc"):
			checklearn(values)
		find_letter(im,end_x+1,0,lc)

def define_letter(im):
	horizontal_cells = 10
	vertical_cells = 10
	horizontal_ratio = im.size[0]//horizontal_cells
	vertical_ratio = im.size[1]//vertical_cells
	values = []
	for i in range(horizontal_cells):
		for j in range(vertical_cells):
			cellsum=0
			for x in range(horizontal_ratio):
				for y in range(vertical_ratio):
					cellsum+=im.getpixel(((i*horizontal_ratio)+x,(j*vertical_ratio)+y))[0]
			cellvalue = cellsum//(horizontal_ratio*vertical_ratio)
			values.append(cellvalue)
	return values

def learn(values,meaning):
	dictionary = open("dictionary", "a")
	dictionary.write("{0}:".format(meaning))
	for value in values:
		dictionary.write("{0},".format(value))
	dictionary.write("\n")
	dictionary.close()

def checklearn(values):
	global output
	dictionary = open("dictionary", "r")
	lowest = 90000000 #some high number
	letter = "A"
	for line in dictionary:
		test_letter = line.split(":")[0]
		test_values = line.split(":")[1]
		test_values=test_values.split(",")
		sum_so_far = 0
		for i in range(len(test_values)-1):
			if(values[i]>int(test_values[i])):
				sum_so_far+=values[i]-int(test_values[i])
			elif(values[i]<int(test_values[i])):
				sum_so_far+=int(test_values[i])-values[i]
			else:
				sum_so_far+=0
		if(sum_so_far<lowest):
			letter = test_letter
			lowest=sum_so_far
	output+=letter
	right = input("{0}(y/n): ".format(letter))
	if (right.lower()=="y"):
		learn(values,letter)
	elif (right.lower()=="n"):
		learn(values, input("Enter actual letter:"))

def check(values):
	global output
	dictionary = open("dictionary", "r")
	lowest = 90000000 #some high number
	letter = "A"
	for line in dictionary:
		test_letter = line.split(":")[0]
		test_values = line.split(":")[1]
		test_values=test_values.split(",")
		sum_so_far = 0
		for i in range(len(test_values)-1):
			if(values[i]>int(test_values[i])):
				sum_so_far+=values[i]-int(test_values[i])
			elif(values[i]<int(test_values[i])):
				sum_so_far+=int(test_values[i])-values[i]
			else:
				sum_so_far+=0
		if(sum_so_far<lowest):
			letter = test_letter
			lowest=sum_so_far
	output+=letter
normalize(im,lower_bound)
lc = input("Learn (l) or check (c) or checklearn (lc): ")
find_letter(im, 0, 0,lc)
print(output)
#monotrans(im,lower_bound)
#crop(im)