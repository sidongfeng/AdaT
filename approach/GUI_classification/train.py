
from __future__ import print_function, division

import _init_paths
import random
import argparse
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import numpy as np
import torchvision
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import time
import os
import copy

from customvision.datasets import ImageFolderWithPaths
from util import get_logger, count_parameters
from modules.BinaryUI import BinaryUI

global logger


def get_args(description='GUI Rendering State Classification'):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--do_pretrain", action='store_true', help="Whether to run training.")
    parser.add_argument("--do_train", action='store_true', help="Whether to run training.")
    parser.add_argument("--do_eval", action='store_true', help="Whether to run eval on the dev set.")

    parser.add_argument('--data_path', type=str, default='hymenoptera_data',
                        help='image file path')
    parser.add_argument('--model_name', type=str, default='resnet18',
                        help='model name to train')
    parser.add_argument('--lr', type=float, default=0.001, help='initial learning rate')
    parser.add_argument('--epochs', type=int, default=25, help='upper epoch limit')
    parser.add_argument('--batch_size', type=int, default=16, help='batch size')
    parser.add_argument('--batch_size_val', type=int, default=1, help='batch size eval')
    parser.add_argument('--num_workers', type=int, default=1, help='number of workers')

    parser.add_argument('--seed', type=int, default=42, help='random seed')
    parser.add_argument('--n_gpu', type=int, default=1, help="Changed in the execute process.")

    parser.add_argument("--output_dir", default=None, type=str, required=True,
                        help="The output directory where the model predictions and checkpoints will be written.")
    parser.add_argument("--init_model", default=None, type=str, required=False, help="Initial model.")

    args = parser.parse_args()

    # Check paramenters
    if not args.do_train and not args.do_eval:
        raise ValueError("At least one of `do_train` or `do_eval` must be True.")

    return args

def set_seed_logger(args):
    global logger
    # predefining random initial seeds
    random.seed(args.seed)
    os.environ['PYTHONHASHSEED'] = str(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)  # if you are using multi-GPU.
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True


    logger = get_logger(os.path.join(args.output_dir, "log.txt"))

    logger.info("Effective parameters:")
    for key in sorted(args.__dict__):
        logger.info("  <<< {}: {}".format(key, args.__dict__[key]))

    return args

def init_device(args):
    global logger

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    n_gpu = torch.cuda.device_count()
    logger.info("device: {} n_gpu: {}".format(device, n_gpu))
    args.n_gpu = n_gpu

    # if args.batch_size % args.n_gpu != 0 or args.batch_size_val % args.n_gpu != 0:
    #     raise ValueError("Invalid batch_size/batch_size_val and n_gpu parameter: {}%{} and {}%{}, should be == 0".format(
    #         args.batch_size, args.n_gpu, args.batch_size_val, args.n_gpu))

    return device, n_gpu

def init_model(args, device):

    if args.init_model:
        model_state_dict = torch.load(args.init_model, map_location='cpu')
    else:
        model_state_dict = None

    # Prepare model
    binaryUI = BinaryUI(n_class=2, model_name=args.model_name, pretrained=args.do_pretrain, state_dict=model_state_dict)
    model = binaryUI.get_model()
    logger.info("  <<< number of parameters: {}".format(count_parameters(model)))

    model.to(device)

    return model

data_transforms = {
    'train': transforms.Compose([
        transforms.Resize((768, 448)), # 768, 448
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    'val': transforms.Compose([
        transforms.Resize((768, 448)),
        # transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
}

def dataloader_train(args):
    image_datasets = datasets.ImageFolder(os.path.join(args.data_path, 'train'),
                                            data_transforms['train'])
    dataloaders = torch.utils.data.DataLoader(image_datasets, batch_size=args.batch_size,
                                                shuffle=True, num_workers=args.num_workers)
    dataset_sizes = len(image_datasets)
    class_names = image_datasets.classes
    return dataloaders, dataset_sizes, class_names

def dataloader_test(args):
    image_datasets = ImageFolderWithPaths(os.path.join(args.data_path, 'val'),
                                            data_transforms['val'])
    dataloaders = torch.utils.data.DataLoader(image_datasets, batch_size=args.batch_size_val,
                                                shuffle=False, num_workers=args.num_workers)
    dataset_sizes = len(image_datasets)
    class_names = image_datasets.classes
    return dataloaders, dataset_sizes, class_names


def save_model(epoch, args, model, type_name=""):
    # Only save the model it-self
    model_to_save = model.module if hasattr(model, 'module') else model
    output_model_file = os.path.join(
        args.output_dir, "pytorch_model.bin.{}{}".format("" if type_name=="" else type_name+".", epoch))
    torch.save(model_to_save.state_dict(), output_model_file)
    logger.info("Model saved to %s", output_model_file)
    return output_model_file


def train_epoch(epoch, args, model, train_dataloader, train_length, device, n_gpu, optimizer, criterion, scheduler):
    global logger
    torch.cuda.empty_cache()
    model.train()
    start_time = time.time()
    total_loss = 0
    total_correct = 0

    for step, batch in enumerate(train_dataloader):
        batch = tuple(t.to(device=device) for t in batch)
        inputs, labels = batch

        optimizer.zero_grad()
        outputs = model(inputs)
        _, preds = torch.max(outputs, 1)
        loss = criterion(outputs, labels)

        # if n_gpu > 1:
        #     loss = loss.mean()  # mean() to average on multi-gpu.
        loss.backward()
        optimizer.step()

        total_loss += loss.item() * inputs.size(0)
        total_correct += torch.sum(preds == labels.data)
        


    scheduler.step()  # Update learning rate schedule
    epoch_loss = total_loss / train_length
    epoch_acc = total_correct.double() / train_length

    logger.info("Epoch: %d/%s, Step: %d/%d, Lr: %s, Loss: %f, Accuracy: %f, Time/step: %f", epoch + 1,
                        args.epochs, step + 1,
                        len(train_dataloader), args.lr,
                        float(epoch_loss),
                        float(epoch_acc),
                        (time.time() - start_time))
        

def eval_epoch(args, model, test_dataloader, test_length, class_names, device, n_gpu):
    if hasattr(model, 'module'):
        model = model.module.to(device)
    model.eval()
    #GPU-WARM-UP
    dummy_input = torch.randn(1, 3, 768, 448, dtype=torch.float).to(device)
    for _ in range(10):
        _ = model(dummy_input)

    all_result_lists = []
    all_label_lists = []
    all_path_lists = []
    total_correct = 0
    total_time = 0
    for batch in test_dataloader:
        inputs, labels, paths = batch
        inputs = inputs.to(device)
        labels = labels.to(device)

        with torch.no_grad():
            start_time = time.time()
            outputs = model(inputs)
            total_time += time.time() - start_time
            _, preds = torch.max(outputs, 1)
            total_correct += torch.sum(preds == labels.data)

            all_result_lists.extend(preds)
            all_label_lists.extend(labels)
            all_path_lists.extend(paths)

    # Save full results
    hyp_path = os.path.join(args.output_dir, "hyp_results.txt")
    with open(hyp_path, "w", encoding='utf-8') as writer:
        for test_data in zip(all_result_lists, all_label_lists, all_path_lists):
            # "predict", "label", "path"
            writer.write("{}\t{}\t{}\n".format(class_names[test_data[0].item()], class_names[test_data[1].item()], test_data[2]))
    logger.info("File of complete results is saved in {}".format(hyp_path))


    # Evaluate
    epoch_acc = total_correct.double() / test_length
    logger.info(">>>  Accuracy: {:.4f}".format(epoch_acc))
    inference_time = total_time / test_length
    logger.info(">>>  Inference time: {:.4f}".format(inference_time))

    return epoch_acc



def main():
    global logger
    args = get_args()
    args = set_seed_logger(args)
    device, n_gpu = init_device(args)
    model = init_model(args, device)

    optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=0.9)
    scheduler = lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)
    criterion = nn.CrossEntropyLoss()

    if args.do_train:
        train_dataloader, train_length, class_names = dataloader_train(args)
        test_dataloader, test_length, _ = dataloader_test(args)
        

        logger.info("***** Running training *****")
        logger.info("  Num examples = %d", train_length)
        logger.info("  Batch size = %d", args.batch_size)
        logger.info("  Class labels = %s", ','.join(class_names))

        best_score = 0.00001
        best_output_model_file = None
        for epoch in range(args.epochs):
            train_epoch(epoch, args, model, train_dataloader, train_length, device, n_gpu, optimizer, criterion, scheduler)

            output_model_file = save_model(epoch, args, model, type_name="")
            accuracy = eval_epoch(args, model, test_dataloader, test_length, class_names, device, n_gpu)
            if best_score <= accuracy:
                best_score = accuracy
                best_output_model_file = output_model_file
            logger.info("The best model is: {}, the Accuracy is: {:.4f}".format(best_output_model_file, best_score))


    elif args.do_eval:
        test_dataloader, test_length, class_names = dataloader_test(args)

        logger.info("***** Running testing *****")
        logger.info("  Num examples = %d", test_length)
        logger.info("  Batch size = %d", args.batch_size_val)

        accuracy = eval_epoch(args, model, test_dataloader, test_length, class_names, device, n_gpu)


if __name__ == "__main__":
    main()