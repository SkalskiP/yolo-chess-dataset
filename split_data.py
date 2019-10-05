#!/usr/bin/python

from os import listdir
from os.path import isfile, join
import argparse
from typing import List
import random

class DataSplit:
    def __init__(self, images_dir_path: str, prefix: str):
        self.images_dir_path = images_dir_path
        self.file_names = self.list_files(images_dir_path)
        self.prefix = prefix

    # List files from labels dir
    @staticmethod
    def list_files(dir_path: str) -> List[str]:
        return [f for f in listdir(dir_path) if isfile(join(dir_path, f))]

    # Saves list items to file - each item in a new line
    @staticmethod
    def save_to_file(list: List[str], file_path: str):
        with open(file_path, 'w') as f:
            f.write("\n".join(list))

    def split(self, train_split: float):
        split_value = round(len(self.file_names) * (1 - train_split))
        file_paths = [self.prefix + file_name for file_name in self.file_names]
        random.shuffle(file_paths)

        train_set = file_paths[:split_value]
        test_set = file_paths[split_value:]

        self.save_to_file(train_set, "chess_train.txt")
        self.save_to_file(test_set, "chess_test.txt")


# Setting parameters
parser = argparse.ArgumentParser()
parser.add_argument('--images-dir', type=str, default='./images', help='path to the dir containing images')
parser.add_argument('--prefix', type=str, default='./data/chess/images/', help='prefix that should precede the name of each file')
parser.add_argument('--train-split', type=float, default=0.25, help='percentage of data that will be included in the training set')

opt = parser.parse_args()
print(opt, "\n")

data_splitter = DataSplit(opt.images_dir, opt.prefix)
data_splitter.split(opt.train_split)