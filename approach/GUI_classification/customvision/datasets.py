import torch
from torchvision import datasets, transforms

class ImageFolderWithPaths(datasets.ImageFolder):
    """Custom dataset that includes image file paths. Extends
    torchvision.datasets.ImageFolder
    """

    # override the __getitem__ method. this is the method that dataloader calls
    def __getitem__(self, index):
        # this is what ImageFolder normally returns 
        original_tuple = super(ImageFolderWithPaths, self).__getitem__(index)
        # the image file path
        path = self.imgs[index][0]
        # make a new tuple that includes original and the path
        tuple_with_path = (original_tuple + (path,))
        return tuple_with_path


if __name__ == "__main__":
    # EXAMPLE USAGE:
    # instantiate the dataset and dataloader
    data_dir = "data"
    dataset = ImageFolderWithPaths(data_dir, transforms.ToTensor()) # our custom dataset
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=1)

    # iterate over data
    for i, data in enumerate(dataloader):
        images,labels,paths = data
        print(paths[0])
        break