
from __future__ import print_function, division

import _init_paths
import random
import argparse
import torch
import numpy as np
from torchvision import transforms
import time
import os
from PIL import Image
import glob

from modules.BinaryUI import BinaryUI

CLASS_NAMES = ['stable', 'unstable'] # make sure the order of class names



def get_args(description='GUI Rendering State Classification'):
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--data_path', type=str, default='hymenoptera_data',
                        help='image file path')
    parser.add_argument('--model_name', type=str, default='resnet18',
                        help='model name to train')

    parser.add_argument('--seed', type=int, default=42, help='random seed')
    parser.add_argument('--n_gpu', type=int, default=1, help="Changed in the execute process.")

    parser.add_argument("--init_model", default=None, type=str, required=True, help="Initial model.")

    args = parser.parse_args()

    return args

def set_seed_logger(args):
    # predefining random initial seeds
    random.seed(args.seed)
    os.environ['PYTHONHASHSEED'] = str(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)  # if you are using multi-GPU.
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True

    return args

def init_device(args):

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    n_gpu = torch.cuda.device_count()
    args.n_gpu = n_gpu

    return device, n_gpu

def init_model(args, device):

    if args.init_model:
        model_state_dict = torch.load(args.init_model, map_location='cpu')
    else:
        model_state_dict = None

    # Prepare model
    binaryUI = BinaryUI(n_class=2, model_name=args.model_name, pretrained=False, state_dict=model_state_dict)
    model = binaryUI.get_model()

    model.to(device)

    return model

data_transforms = transforms.Compose([
        transforms.Resize((768, 448)),
        # transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])



def main():
    args = get_args()
    args = set_seed_logger(args)
    device, n_gpu = init_device(args)
    model = init_model(args, device)

    if hasattr(model, 'module'):
        model = model.module.to(device)
    
    model.eval()

    all_result_lists = []
    all_path_lists = []
    total_time = []
    for img_path in (glob.glob(os.path.join(args.data_path, '*.jpg'))
                        + glob.glob(os.path.join(args.data_path, '*.png'))):
        start_time = time.time()
        img = Image.open(img_path)
        img = data_transforms(img).unsqueeze(0)
        
        img = img.to(device)

        with torch.no_grad():
            outputs = model(img)
            _, preds = torch.max(outputs, 1)
            time_spend = time.time() - start_time
            total_time.append(time_spend)
            print('>>> {}: {:.3f}'.format(img_path, time_spend))

            all_path_lists.append(img_path)
            all_result_lists.append(CLASS_NAMES[preds[0].item()])

    # Save full results
    hyp_path = os.path.join(args.data_path, "prediction_results.txt")
    with open(hyp_path, "w", encoding='utf-8') as writer:
        for test_data in zip(all_result_lists, all_path_lists):
            # "predict", "path"
            writer.write("{}\t{}\n".format(test_data[0], test_data[1]))

    print('>>> Total {} images, average time spent: {:.3f}'
                            .format(len(all_result_lists), sum(total_time[1:])/(len(all_result_lists)-1)))

if __name__ == "__main__":
    main()