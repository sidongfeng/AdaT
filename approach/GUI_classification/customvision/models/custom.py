import torch
import torch.nn as nn
import torch.nn.functional as F

class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 64, (7,7))
        self.pool = nn.MaxPool2d(kernel_size=3)
        self.conv2 = nn.Conv2d(64, 512, (3,3))
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512, 100)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)
        return x

def cnn():
    return CNN()

# batch = torch.rand(1, 3, 768, 448)
# net = CNN()
# print(net)

# outputs = net(batch)
# print(outputs.shape)