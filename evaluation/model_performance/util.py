import os
import torch
import torch.nn as nn
import threading
from torch._utils import ExceptionWrapper
import logging

def get_logger(filename=None):
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(format='%(asctime)s - %(levelname)s -   %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO)
    if filename is not None:
        handler = logging.FileHandler(filename)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
        logging.getLogger().addHandler(handler)
    return logger

def remove_bad_images():
    for split in ['train', 'val']:
        for class_ in ['ants', 'bees']:
            for img_path in os.listdir(f'/user-data/hymenoptera_data/{split}/{class_}'):
                if img_path.startswith('._'):
                    os.remove(f'/user-data/hymenoptera_data/{split}/{class_}/{img_path}')
                    print(img_path)

def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)