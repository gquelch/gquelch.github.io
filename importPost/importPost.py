# I use this script to process Markdown files export from Notion
# - adds front matter
# - remap image paths
# - renames post with date
# - adds escapes for underscores
# - moves post to appropriate directory
# - moves images to the appropriate directory

import os
import sys
import datetime
import fileinput
import shutil

inputCMD = " ".join(sys.argv[1:])

importDirectory = "/home/pi/github/gquelch.github.io/postImport"

imagePath = "/assets/post_images/"
imageDirectory = "/home/pi/github/gquelch.github.io/assets/post_images/"
postDirectory = "/home/pi/github/gquelch.github.io/_posts"

def GQ_detectFiles():
	
	files = os.listdir(importDirectory)
	for file in files:
		if file.endswith(".md"):
		
			if inputCMD == "1":		
				fileSplit = file.split()
				folderNameOrig = file.split(".")[0]
				
				
				postName = " ".join(fileSplit[:-1])

				os.rename(file,postName + ".md")
				
				if (os.path.isdir(folderNameOrig)) == True:
					os.rename(folderNameOrig,postName)
					
			else:
				postName = file.split(".")[0]



			GQ_NotionToJekyll(postName)


def GQ_NotionToJekyll(inputName):	
	today = str(datetime.date.today())
	
	inputPost = inputName + ".md"
	
	s = "-"
	newFileName = today + "-" + inputPost.replace(" ","-")

	oldFile = open(inputPost,"r")
	newFile = open(newFileName,"w+")
	
	frontMatter = ("---" + "\n" +
	"*" + 
	"layout: post" + "\n" +
	"published: true" + "\n" +
	"---")
	

	
	oldFileLines = oldFile.readlines()
	oldFileLen = len(oldFileLines) 	

	for i in range(oldFileLen):
	
		# Get title from first line, add it to Front Matter #
		if i == 0:
			if oldFileLines[i].startswith("#"):
				title = "title: " + oldFileLines[i][2:]
				
				frontMatter = frontMatter.replace("*",title)
				
				newFile.write(frontMatter)
				
		# Prefx Image Paths #
		elif oldFileLines[i].startswith("!"):
			#lineImagePath = oldFileLines[i].replace("(",imagePath)
			
			imagePathOrig = oldFileLines[i].split("(")[1]
			imageName = imagePathOrig.split("/")[1][:-2]
			
			image = inputName.replace(" ","%20") + "/" + imageName
			
			lineImagePath = "<img src=\"" + imagePath + image + "\" class = \"responsive-image\"/>" 

			newFile.write(lineImagePath)
			newFile.write("\n")
			
		# Notion Database Data Pass #
		elif oldFileLines[i].startswith("Created:") or oldFileLines[i].startswith("Published:") or oldFileLines[i].startswith("Status:"):
			pass
			
		# Underscore Markdown Escape "
		elif "_" in oldFileLines[i]:
		
			#ignore links
			if "[" in oldFileLines[i]:
				pass
				
			else:
				lineFixUnderscore = oldFileLines[i].replace("_","\_")
				
				newFile.write(lineFixUnderscore)
			
		# Add standard lines to new file
		else:
			newFile.write(oldFileLines[i])
			
	
	oldFile.close()
	newFile.close()
	
	os.rename(newFileName, postDirectory + "/" + newFileName)
	shutil.move(inputName,imageDirectory)
	os.remove(inputPost)


GQ_detectFiles()