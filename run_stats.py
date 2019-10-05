#!/usr/bin/python

from os import listdir
from os.path import isfile, join
import argparse
from typing import List, Dict

class YoloStats:
    def __init__(self, names_file_path):
        self.names_file_path = names_file_path
        self.label_names = self.load_label_names(names_file_path)
        self.labels_counter = self.init_labels_counter(self.label_names)

    # Load label names
    @staticmethod
    def load_label_names(file_path: str) -> List[str]:
        with open(file_path, 'r') as f:
            return f.read().splitlines()

    # List files from labels dir
    @staticmethod
    def list_files(dir_path: str) -> List[str]:
        return [join(dir_path, f) for f in listdir(dir_path) if isfile(join(dir_path, f))]

    # Initiate labels counter
    @staticmethod
    def init_labels_counter(label_names: List[str]) -> Dict:
        return { name : 0 for name in label_names }

    # Map label index to label name
    def get_label_name(self, index: int) -> str:
        return self.label_names[index]

    # Calculate stats
    def calculate(self, dir_path: str):
        file_paths = self.list_files(dir_path)
        for file_path in file_paths:
            self.update_with_labels(file_path)

    # Update counters with labels
    def update_with_labels(self, lablels_file_path: str):
        with open(lablels_file_path, 'r') as f:
            for line in f:
                label_name = self.get_label_name(int(line.split()[0]))
                self.labels_counter[label_name] += 1

    # Print stats
    def print_stats(self):
        for key, value in self.labels_counter.items():
            print (key, ':\t', value)


# Setting parameters
parser = argparse.ArgumentParser()
parser.add_argument('--labels-dir', type=str, default='./labels', help='path to the dir containing the yolo labels')
parser.add_argument('--names', type=str, default='names.txt', help='path to the file containing label names')

opt = parser.parse_args()
print(opt, "\n")

stats = YoloStats(opt.names)
stats.calculate(opt.labels_dir)
stats.print_stats()