from __future__ import print_function, division
from torchvision import transforms
import time
import torch
from PIL import Image

from .model.BinaryUI import BinaryUI

CLASS_NAMES = ['stable', 'unstable'] # make sure the order of class names
data_transforms = transforms.Compose([
            transforms.Resize((768, 448)),
            # transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])


class Classifer(object):
    def __init__(self, init_model, model_name):
        model_state_dict = torch.load(init_model, map_location='cpu')
        binaryUI = BinaryUI(n_class=2, model_name=model_name, pretrained=False, state_dict=model_state_dict)
        self.model = binaryUI.get_model()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        if hasattr(self.model, 'module'):
            self.model = self.model.module.to(self.device)
        self.model.eval()
    
    def model_warmup(self):
        for _ in range(5):
            img = torch.ones(1, 3, 768, 448)
            img = img.to(self.device)
            with torch.no_grad():
                _ = self.model(img)
    
    def loading_img_path(self, img_path):
        img = Image.open(img_path).convert('RGB')
        img = data_transforms(img).unsqueeze(0)
        img = img.to(self.device)
        return img

    def predict(self, img_path):
        start_time = time.time()
        img = self.loading_img_path(img_path)
        # img = data_transforms(img).unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs = self.model(img)
            _, preds = torch.max(outputs, 1)
            class_name = CLASS_NAMES[preds[0].item()]
            time_spend = time.time() - start_time
            print(' >>> Predicting {} in {:.2f} ms ---- {}'.format(img_path.split('temp')[-1], time_spend*1000, class_name))

        return preds[0].item()


# init_model = '/Users/mac/Documents/Python/binaryUI/approach/model_prediciton/output/01-27-21.41.34/pytorch_model.bin.3'
# model_name = 'resnet18'
# img_path = '/Users/mac/Documents/Python/binaryUI/approach/model_prediciton/inference/step-63--g0a94-1644312401994.png'
# classifer = Classifer(init_model, model_name)
# classifer.predict(img_path)