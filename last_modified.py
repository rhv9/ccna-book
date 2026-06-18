import json
import sys
import logging
import os
import time
import subprocess
import datetime

class FileLogger:
    def __init__(self, log_file: str, log_level: int = logging.INFO):
        self.log_file = log_file

        # Create the logger
        self.logger = logging.getLogger('FileLogger')
        self.logger.setLevel(log_level)

        # Ensure we don't add multiple handlers if this is called multiple times
        if not self.logger.handlers:
            if os.path.exists(log_file):
                os.remove(log_file)

            # Create the file handler
            file_handler = logging.FileHandler(self.log_file)
            file_handler.setLevel(log_level)

            # Create a formatter and set it for the handler
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)

            # Add the handler to the logger
            self.logger.addHandler(file_handler)

    def print(self, message: str):
        self.logger.info(message)

def recursiveAddCommitTime(items):
    for section in items:
        if section == "Separator" or section == None:
            continue
        
        chapterName = section['Chapter']['name']
        chapterPath = section['Chapter']['source_path']

        if chapterPath != None:
            file_path = "./pages/" + chapterPath
            process = subprocess.run(["git", "log", "-1", "--format=%cd", file_path], capture_output=True)
            
            # This is using last modified time from file
            # mtime = os.path.getmtime(file_path)
            # mTimeString = time.ctime(mtime)
            # readableElapsedTime = getReadableTimeAgo(time.time(), mtime)
            
            readableElapsedTime = ""
            mTimeString = str(process.stdout)[2:-2]
            if len(mTimeString) == 0:
                readableElapsedTime = "no commit"
            else:
                readableElapsedTime = mTimeString
                
            section['Chapter']['content'] = "*last modified: "+" ("+readableElapsedTime+")*\n\n" + section['Chapter']['content']

        chapterSubItems = section['Chapter']['sub_items']

        if len(chapterSubItems) != 0:
            recursiveAddCommitTime(chapterSubItems)


if __name__ == '__main__':
    if len(sys.argv) > 1: # we check if we received any argument
        if sys.argv[1] == "supports": 
            # then we are good to return an exit status code of 0, since the other argument will just be the renderer's name
            sys.exit(0)

    # load both the context and the book representations from stdin
    context, book = json.load(sys.stdin)
    
    # Dump json
    # f = open("jsonDump.json", "w")
    # f.write(json.dumps(book))
    
    # Debugging printer
    logger = FileLogger("preprocessor.log")

    recursiveAddCommitTime(book['sections'])
    
    # we are done with the book's modification, we can just print it to stdout, 
    print(json.dumps(book)) 