import os
from random import random

class FileReader(object):
    """FileReader object, handles all file operations"""
    def __init__(self):
        super(FileReader, self).__init__()
        # lists of filenames for positive and negative sample training sets
        self.eights = []
        self.others = []
        # pointers within those lists
        self.eightPtr = 0
        self.otherPtr = 0
        # boolean for selecting randomly from either positive or negative samples
        self.coin = True
        self.TRAINING_SIZE = 0
        # populate filename lists
        for root, dirs, files in os.walk('./data/train8'):
            self.eights = files
            self.TRAINING_SIZE += len(files)
        for root, dirs, files in os.walk('./data/trainOthers'):
            self.others = files
            self.TRAINING_SIZE += len(files)


    """Randomly picks and reads a file from the training data"""
    def next_file(self):
        # "coin flip", accounts for cases when one of the lists might have been finished
        self.coin = (self.eightPtr < len(self.eights) and random() > 0.5) or self.otherPtr >= len(self.others)
        filename = "./data/"
        # based on coin, randomly selects either a positive or negative sample
        if self.coin:
            filename += "train8/" + self.eights[self.eightPtr]
            self.eightPtr += 1
        else:
            filename += "trainOthers/" + self.others[self.otherPtr]
            self.otherPtr += 1

        with open(filename) as f:
            return [list(line) for line in f.read().split("\n")[:-1]]


    """Gets the label associated with the currently picked file"""
    def get_label(self):
        # uses the pointers to read the correct label file
        # based on earlier coin flip
        if self.coin:
            with open("./data/label8/" + self.eights[self.eightPtr-1]) as f:
                return f.read()
        else:
            with open("./data/labelOthers/" + self.others[self.otherPtr-1]) as f:
                return f.read()


    """Resets the pointers into the sample lists"""
    def reset(self):
        self.eightPtr = 0
        self.otherPtr = 0


    """Reads custom image file supplied by user"""
    def read_image_file(self, filename):
        with open(filename) as f:
            return [list(line) for line in f.read().split("\n")[:-1]]
