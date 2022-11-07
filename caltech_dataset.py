from torchvision.datasets import VisionDataset

from PIL import Image

import os
import os.path
import sys


def pil_loader(path):
    # open path as file to avoid ResourceWarning (https://github.com/python-pillow/Pillow/issues/835)
    with open(path, 'rb') as f:
        img = Image.open(f)
        return img.convert('RGB')


class Caltech(VisionDataset):
    def __init__(self, root, split='train', transform=None, target_transform=None):
        super(Caltech, self).__init__(root, transform=transform, target_transform=target_transform)
        

        self.split = split # This defines the split you are going to use
                           # (split files are called 'train.txt' and 'test.txt')

        path = "/content/Caltech101/" + self.split + ".txt"

        self.data = list()
        self.labels = set()
        
        with open(path, 'r') as f:
            for line in f:
                image_path = "/content/" + root + '/' + line.strip()
                label = line.strip().split('/')[0]
                image = pil_loader(image_path)
                if "BACKGROUND_Google" not in label:
                    self.labels.add(label)
                    self.data.append((image, list(self.labels).index(label)))

    def __getitem__(self, index):
        '''
        __getitem__ should access an element through its index
        Args:
            index (int): Index
        Returns:
            tuple: (sample, target) where target is class_index of the target class.
        '''

        image, label = self.data[index]

        # Applies preprocessing when accessing the image
        if self.transform is not None:
            image = self.transform(image)

        return image, label

    def __len__(self):
        '''
        The __len__ method returns the length of the dataset
        It is mandatory, as this is used by several other components
        '''
        return len(self.data)
