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

inputName = " ".join(sys.argv[1:])

print ""

imagePath = "(/assets/post_images/"
imageDirectory = "/home/pi/github/git_edit/assets/post_images/"
postDirectory = "/home/pi/github/git_edit/_posts"

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
	
		# Get title, add it to Front Matter and add to new file
		if i == 0:
			if oldFileLines[i].startswith("#"):
				title = "title: " + oldFileLines[i][2:]
				
				frontMatter = frontMatter.replace("*",title)
				
				newFile.write(frontMatter)
				
		# Get image paths, add folder structure prefix, add to new file
		elif oldFileLines[i].startswith("!"):
			lineImagePath = oldFileLines[i].replace("(",imagePath)
			
			newFile.write(lineImagePath)
			
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

GQ_NotionToJekyll(inputName)