from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import torch
from torch import nn
import torch.nn.functional as F
from torch.nn import CrossEntropyLoss, MSELoss

from customvision.models import resnet, custom
from torchvision import models

class BinaryUI():
    """ An abstract class to handle weights initialization and
        a simple interface for dowloading and loading pretrained models.
    """
    def __init__(self, n_class, model_name, pretrained, state_dict=None):
        # utilize bert config as base config
        super(BinaryUI, self).__init__()
        self.n_class = n_class
        self.pretrained = pretrained
        self.state_dict = state_dict
        self.model_name = model_name

        # print(self.n_class, self.pretrained, self.state_dict)

        if self.model_name == 'resnet18':
            # self.model = resnet.resnet18(pretrained=self.pretrained)
            self.model = models.resnet18(pretrained=self.pretrained)
            num_ftrs = self.model.fc.in_features
            self.model.fc = nn.Linear(num_ftrs, n_class)
        elif self.model_name == 'mobilenet':
            self.model = models.mobilenet_v2(pretrained=self.pretrained)
            num_ftrs = self.model.classifier[1].in_features
            self.model.classifier[1] = nn.Linear(num_ftrs, n_class)
        elif self.model_name == 'mobilenet_small':
            self.model = models.mobilenet_v3_small(pretrained=self.pretrained)
            num_ftrs = self.model.classifier[3].in_features
            self.model.classifier[3] = nn.Linear(num_ftrs, n_class)
        elif self.model_name == 'custom':
            self.model = custom.cnn()
            num_ftrs = self.model.fc.in_features
            self.model.fc = nn.Linear(num_ftrs, n_class)
        elif self.model_name == 'efficientnet':
            from efficientnet_pytorch import EfficientNet
            self.model = EfficientNet.from_pretrained('efficientnet-b0', num_classes=n_class)

        if state_dict is not None:
            self.model.load_state_dict(state_dict)

    def get_model(self):
        return self.model
