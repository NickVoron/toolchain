#!/usr/bin/env python3
import signal
import subprocess
import contextlib
import logging
import os
import shutil
import re
from template import collect_files
from datetime import datetime
from pathlib import Path
from email import utils
from os import listdir
from os.path import isfile, join

command = ["hg", "log" ]

@contextlib.contextmanager
def cwd(new_cwd):
    """Context manager for current working directory."""
    old_cwd = Path.cwd()
    logging.info('Change cwd: %s', str(new_cwd))
    os.chdir(str(new_cwd))
    yield
    logging.info('Restore cwd: %s', str(old_cwd))
    os.chdir(str(old_cwd))

publishingDir = Path('../publishing0')
fileExceptions = set(line.replace('\\', '/').strip() for line in open('sources_exceptions.txt'))
thirdPartyExceptions = set(line.replace('\\', '/').strip() for line in open('third_party_exceptions.txt'))

cpp_sources = ["c", "cc", "cpp", "cxx", "h", "hh", "hpp", "hxx"]

with open ('license_header.txt', "r") as src:
    headerText = src.read()

with open ('license_footer.txt', "r") as src:
    footerText = src.read()

with open ('license_file_footer.txt', "r") as src:
    endingText = src.read()

uniqueAuthors = dict([
    (r'Voronetskiy Nikolay <voronetskiy.nikolay@gmail.com>' , 'Voronetskiy Nikolay <nikolay.voronetskiy@yandex.ru>'),
    (r'denis.netahin', 'Denis Netakhin <denis.netahin@yandex.ru>'),
    (r'denis.natkhin', 'Denis Netakhin <denis.netahin@yandex.ru>'),
    (r'denis.netakhin', 'Denis Netakhin <denis.netahin@yandex.ru>'),
    (r'n_voronetskiy', 'Voronetskiy Nikolay <nikolay.voronetskiy@yandex.ru>'),
    (r'coolace', 'Voronetskiy Nikolay <nikolay.voronetskiy@yandex.ru>'),
    (r'used@used-HP-Z230-Tower-Workstation', 'Voronetskiy Nikolay <nikolay.voronetskiy@yandex.ru>'),
    (r' Voronetskiy Nikolay', 'Voronetskiy Nikolay <nikolay.voronetskiy@yandex.ru>'),
    (r'strelok', 'Denis Netakhin <denis.netahin@yandex.ru>'),
    (r'Denis Netahin', 'Denis Netakhin <denis.netahin@yandex.ru>'),
    (r'Voronetskiy Nikolay', 'Voronetskiy Nikolay <nikolay.voronetskiy@yandex.ru>')])

CODE = {'A': '.-',     'B': '-...',   'C': '-.-.', 
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
        'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',

        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.' 
        }

CODE_REVERSED = {value:key for key, value in CODE.items()}

def in_directory(file, directory):
    directory = os.path.join(os.path.realpath(directory), '')
    file = os.path.realpath(file)
    return os.path.commonprefix([file, directory]) == directory

def split(s, chunk_size):
    a = zip(*[s[i::chunk_size] for i in range(chunk_size)])
    return [''.join(t) for t in a]

def to_morse(s):
    return ' '.join(CODE.get(i.upper()) for i in s)

def from_morse(s):
    return ''.join(CODE_REVERSED.get(i) for i in s.split())

def removeComments(string):
	string = re.sub(re.compile("/\*.*?\*/", re.DOTALL ) ,"" ,string) # remove all occurance streamed comments (/*COMMENT */) from string
	string = re.sub(re.compile("//.*?\n" ) ,"\n" ,string) # remove all occurance singleline comments (//COMMENT\n ) from string
	return string

def removeCommentsFromFile(filename):
	with open (filename, "r") as src:
		data = src.read()
	with open (filename, "w") as trg:
		trg.write(removeComments(data))

def removeCommentsFromCXX(parentDir, directory):
    for file in collect_files(directory, cpp_sources):
        fileName = str(file).replace(str(parentDir) + '\\', "").replace('\\', '/').strip()
        fileForPublishing = not fileName in fileExceptions
        if fileForPublishing:
            removeCommentsFromFile(file)            

def getAuthor(nickname):
    return uniqueAuthors[nickname]

def getFileAuthors(filePath):
    cmd = command.copy()
    cmd.append(filePath)

    uniqueRects = dict()

    #print("command: " + cmd[0] + " " + cmd[1] + " " + cmd[2]  )
    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
        output = proc.stdout.read().decode("cp1251")
        #logging.info("output size:" + str(len(output)))

        allCommit = output.split("\n\n")

        for record in allCommit:
            if len(record) ==0:
                continue

            detailedInfo = record.split("\n")

            #logging.info(len(detailedInfo))

            user = ""
            date = ""

            if len(detailedInfo) == 4 or len(detailedInfo) == 3 :
                user = detailedInfo[1]
                date = detailedInfo[2]
                #logging.info(detailedInfo[1]+", "+detailedInfo[2])

            elif len(detailedInfo) == 5:
                user = detailedInfo[2]
                date = detailedInfo[3]
                #logging.info(detailedInfo[2]+", "+detailedInfo[3])

            elif len(detailedInfo) == 6:
                user = detailedInfo[3]
                date = detailedInfo[4]
                #logging.info(detailedInfo[3]+", "+detailedInfo[4])
            elif len(detailedInfo) == 7:
                user = detailedInfo[4]
                date = detailedInfo[5]
                #logging.info(detailedInfo[4]+", "+detailedInfo[5)
            else:
                logging.info(detailedInfo)
                assert();

            clearDateStr = date[10:-6].strip()
            #logging.info(user + ", " + clearDateStr)

            author = getAuthor(user.replace('user:        ', ''))
            dateArray = uniqueRects.get(author, [])
            dateArray.append(datetime.strptime(clearDateStr, "%a %b %d %H:%M:%S %Y"))
            uniqueRects[author] = dateArray

        #logging.info("size: "+str(len(uniqueRects)))

    result = {}
    for key in uniqueRects:
        minDate = min(uniqueRects[key])
        maxDate = max(uniqueRects[key])
        #logging.info(key + ", min: " + str(minDate) + ", max: " +str(maxDate))
        result[key] = {"min": minDate, "max": maxDate}

    return  result

def evaluateDir(path):
    if ".hg" in path:
        return
    if ".git" in path:
        return
    if ".svn" in path:
        return
    if ".vs" in path:
        return

    for iter in listdir(path):
        fullPath = path+"\\"+iter

        if not isfile(fullPath):
            evaluateDir(fullPath)
        else:
            filename, fileExt = os.path.splitext(fullPath)
            if fileExt == ".h" or fileExt == ".hh":
                print("================================================================")
                authors = getFileAuthors(fullPath)

                for key in authors:
                    #uniqueAuthors.add(key)
                    print(key + ", min: " + str(authors[key]["min"]) + ", max: " + str(authors[key]["max"]))

                print("================================================================")



# authors = getFileAuthors("Stable/Sources/Libraries/renderPipeline/renderPipeline.cpp")
#
# for key in authors:
#     logging.info(key + ", min: " + str(authors[key]["min"]) + ", max: " + str(authors[key]["max"]))

#evaluateDir(os.path.dirname(os.path.abspath(__file__)))

#evaluateDir('Stable')

def authorsListForFile(authors):
    authorsList = ''
    for key in authors:
        authorsList += key + ", "
    return authorsList[0:-2]

def yearsRangeForFile(authors):
    minYear = 10000
    maxYear = 0    
    for key in authors:
        minYear = min(authors[key]["min"].year, minYear)
        maxYear = max(authors[key]["max"].year, maxYear)
    if minYear == maxYear:
        return str(minYear)

    return str(minYear) + '-' + str(maxYear)

def removeTempDirs(directory):
    if os.path.isdir(Path(directory) / '.vs'):
        shutil.rmtree(Path(directory) / '.vs')

def appendHeadersToCXX(parentDir, directory):
    for file in collect_files(directory, cpp_sources):
        fileName = str(file).replace(str(parentDir) + '\\', "").replace('\\', '/').strip()
        fileForPublishing = (not fileName in fileExceptions)
        for exceptDir in fileExceptions:
        	if os.path.isdir(exceptDir):
        		if(in_directory(fileName, exceptDir)):
        			fileForPublishing = False
        			break

        if not fileForPublishing:
            print("skipped file:", fileName)
        else :
            authors = getFileAuthors(fileName)
            authorsCopyright = "// Copyright (C) " + yearsRangeForFile(authors) + " " + authorsListForFile(authors) + "\n"
            resultHeader = ""
            resultHeader += authorsCopyright
            resultHeader += footerText
            with open (file, "r+") as src:
                content = src.read()
                src.seek(0, 0)
                src.write(resultHeader + "\n" + content + "\n\n\n\n")
                src.write(authorsCopyright)
                src.write(endingText)
            print("published file:", fileName, os.path.dirname(fileName))

def publishSourceDir(directory):
    print('publishing directory:', directory)
    resultDir = publishingDir / directory
    removeTempDirs(directory)
    shutil.copytree(directory, resultDir)
    removeCommentsFromCXX(publishingDir, resultDir)
    appendHeadersToCXX(publishingDir, resultDir)

def copySourceDir(rootDirectory):
    for root, dirs, files in os.walk(rootDirectory):
        for directory in dirs:
            directory = (rootDirectory + '/' + directory).replace('\\', '/')
            directoryForPublishing = not directory in thirdPartyExceptions
            if not directoryForPublishing:
                print("skipped directory:", directory)
            else :
                print('copy directory:', directory)
                resultDir = publishingDir / directory
                removeTempDirs(directory)
                shutil.copytree(directory, resultDir)
        for file in files:
            file = (rootDirectory + '/' + file).replace('\\', '/')
            resultFile = publishingDir / file
            print('copy file:', file, "to", resultFile)
            if not os.path.exists(os.path.dirname(resultFile)):
                os.makedirs(os.path.dirname(resultFile))
            shutil.copyfile(file, resultFile)
        return

def cleanup():
    print('cleanup old result')
    if os.path.isdir(publishingDir):
        shutil.rmtree(publishingDir)

#encodedRevision = to_morse('8590')
#print(encodedRevision)
#decodedRevision = from_morse(encodedRevision)
#print(decodedRevision)
apppath = '../../'
with cwd(apppath):
    cleanup()
    publishSourceDir('Stable')
    copySourceDir('VS_Props')
    copySourceDir('Tools')
    copySourceDir('third_party')
    copySourceDir('toolchain')