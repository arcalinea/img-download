# import the necessary packages
# from imutils import paths
import argparse
import requests
import cv2
import os, sys

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--urls", required=True,
    help="path to file containing image URLs")
ap.add_argument("-o", "--output", required=True,
    help="path to output directory of images")
args = vars(ap.parse_args())

directory = args["output"]

def download_imgs():
    # grab the list of URLs from the input file
    rows = open(args["urls"]).read().strip().split("\n")
    img_num = 0
    # loop the URLs
    for url in rows:
        try:
            # try to download the image
            print url
            r = requests.get(url, timeout=60)
            print r
            # save the image to disk
            p = os.path.sep.join([directory, "snowleopard-{}.jpg".format(img_num)])
            print p
            f = open(p, "wb")
            f.write(r.content)
            f.close()
            print("[INFO] downloaded: {}".format(p))
            img_num += 1
            
            # handle if any exceptions are thrown during the download process
        except:
            img_num += 1
            print("[INFO] error downloading {}...skipping".format(p))
    
def openCV_load():
    # loop over the image paths we just downloaded
    for img in os.listdir(directory):
        imagePath = os.path.join(directory, img)
    	# initialize if the image should be deleted or not
    	delete = False
        
    	# try to load the image
    	try:
    		image = cv2.imread(imagePath)
        
    		# if the image is `None` then we could not properly load it
    		# from disk, so delete it
    		if image is None:
    			delete = True
        
    	# if OpenCV cannot load the image then the image is likely
    	# corrupt so we should delete it
    	except:
    		print("Except")
    		delete = True
        
    	# check to see if the image should be deleted
    	if delete:
    		print("[INFO] deleting {}".format(imagePath))
    		os.remove(imagePath)
        
download_imgs()
openCV_load()
