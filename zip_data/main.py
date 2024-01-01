# Load all the things in article_zips
# unzip them and save them in unzip

import os
import zipfile
import bs4
import markdownify

print(__file__)

# Path to the directory containing the zip files
zip_path = 'article_zips'

# Path to the directory where the unzipped files will be saved
unzip_path = 'unzip'

def unzip():
    # Get a list of all the zip files
    zip_files = os.listdir(zip_path)

    # delete everything in the unzip folder
    """ folders = os.listdir(unzip_path)
    for folder in folders:
        os.rmdir(unzip_path + '/' + folder) """

    # Loop through each file
    for file_name in zip_files:
        # Create the full path to the file
        print(file_name)
        full_path = os.path.join(zip_path, file_name)
        
        # Open the zip file
        zip_ref = zipfile.ZipFile(full_path, 'r')
        
        # Extract the files
        zip_ref.extractall(unzip_path + '/' + file_name.split('.')[0].replace(" ", ""))
        
        # Close the zip file
        zip_ref.close()

def load_images_duplicate():
    # Loop through all the directories in the unzip folder
    # Check if they have an images folder
    # if they do copy the images in the folder to the images folder with the name of the directory

    folders = os.listdir(unzip_path)
    print(folders)

    # delete everything in the images folder
    """ images = os.listdir('images')
    for image in images:
        os.remove('images/' + image) """

    for folder in folders:
        if os.path.isdir(unzip_path + '/' + folder + '/images'):
            images = os.listdir(unzip_path + '/' + folder + '/images')
            i = 0
            for image in images:
                i += 1
                if image.endswith('.jpg') or image.endswith('.png'):
                    os.rename(unzip_path + '/' + folder + '/images/' + image, 'images/' + folder + f"-{i}." + image.split('.')[1])
                    print(unzip_path + '/' + folder + '/images/' + image, 'images/' + folder + '.jpg')

def load_markdown_from_html():
    # Loop through all the directories in the unzip folder
    # Check if they have an html folder
    # if they do copy the html in the folder to the markdown folder with the name of the directory

    folders = os.listdir(unzip_path)

    # delete everything in the markdown folder
    markdowns = os.listdir('markdown')
    for markdown in markdowns:
        os.remove('markdown/' + markdown)

    for folder in folders:
        # get whatever html file is there
        html_files = os.listdir(unzip_path + '/' + folder)
        html_file = ''
        for file in html_files:
            if file.endswith('.html'):
                html_file = unzip_path + '/' + folder + '/' + file
                break
        
        with open(html_file, 'r', encoding='utf-8') as html:
            with open('markdown/' + '2024-1-1-' + folder + '.md', 'w', encoding='utf-8') as markdown:
                # get only the body element
                page = html.read()
                soup = bs4.BeautifulSoup(page, 'html.parser')
                body = soup.find('body')
                
                h = markdownify.markdownify(str(body), heading_style="ATX") 

                h = h.replace('images/image', 'assets/images/jan/' + folder)

                # put this text at the top of the file

                text = """---
layout: post
title:  "title"
author: [ author ]
categories: [ Opinion ]
image: assets/images/jan/""" + folder + """.jpg
tags: []
---\n"""
                h = text + h

                markdown.write(h)

""" unzip()
load_images_duplicate() """

load_markdown_from_html()

# unzip()
