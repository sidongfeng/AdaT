import os
import glob
import tqdm
import random
import shutil

from videoscene import VideoScene


ANIMATION_FOLDER = 'Rico/animations'
GESTURE_FOLDER = 'Rico/filtered_traces'
STABLE_DURATION = 1
STALE_THRESHOLD = 0.99
NUM_UNSTABLE = 3
OUTPUT_DIR = './dataset'






def split_dataset(OUTPUT_STABLE_DIR, OUTPUT_UNSTABLE_DIR, OUTPUT_DIR):
    stable_list = glob.glob(f'{OUTPUT_STABLE_DIR}/*.jpg')
    unstable_list = glob.glob(f'{OUTPUT_UNSTABLE_DIR}/*.jpg')
    img_list = unstable_list + stable_list
    apps = [img_path.split('/')[-1].split('-')[0] for img_path in img_list]
    apps = list(set(apps))

    ratio = 0.8
    random.shuffle(apps)

    train_app = random.sample(apps, int(len(apps)*ratio))
    valid_app = random.sample([a for a in apps if a not in apps], int(len([a for a in apps if a not in apps])*0.5))
    train_stable, train_unstable = [], []
    val_stable, val_unstable = [], []
    test_stable, test_unstable = [], []
    for img_path in img_list:
        app = img_path.split('/')[-1].split('-')[0]
        if app in train_app:
            if img_path in stable_list:
                train_stable.append(img_path)
            else:
                train_unstable.append(img_path)
        elif app in valid_app:
            if img_path in stable_list:
                val_stable.append(img_path)
            else:
                val_unstable.append(img_path)
        else:
            if img_path in stable_list:
                test_stable.append(img_path)
            else:
                test_unstable.append(img_path)

    train_dir = os.path.join(OUTPUT_DIR, 'train')
    train_stable_dir = os.path.join(train_dir, 'stable')
    train_unstable_dir = os.path.join(train_dir, 'unstable')
    val_dir = os.path.join(OUTPUT_DIR, 'val')
    val_stable_dir = os.path.join(val_dir, 'stable')
    val_unstable_dir = os.path.join(val_dir, 'unstable')
    test_dir = os.path.join(OUTPUT_DIR, 'test')
    test_stable_dir = os.path.join(test_dir, 'stable')
    test_unstable_dir = os.path.join(test_dir, 'unstable')
    os.mkdir(train_dir)
    os.mkdir(val_dir)
    os.mkdir(test_dir)
    os.mkdir(train_stable_dir)
    os.mkdir(train_unstable_dir)
    os.mkdir(val_stable_dir)
    os.mkdir(val_unstable_dir)
    os.mkdir(test_stable_dir)
    os.mkdir(test_unstable_dir)
    
    for img in train_stable:
        shutil.copyfile(img, '{}/{}'.format(train_stable_dir, img.split('/')[-1]))

    for img in train_unstable:
        shutil.copyfile(img, '{}/{}'.format(train_unstable_dir, img.split('/')[-1]))

    for img in val_stable:
        shutil.copyfile(img, '{}/{}'.format(val_stable_dir, img.split('/')[-1]))

    for img in val_unstable:
        shutil.copyfile(img, '{}/{}'.format(val_unstable_dir, img.split('/')[-1]))

    for img in test_stable:
        shutil.copyfile(img, '{}/{}'.format(test_stable_dir, img.split('/')[-1]))

    for img in test_unstable:
        shutil.copyfile(img, '{}/{}'.format(test_unstable_dir, img.split('/')[-1]))




def main():
    '''
        Construct partially rendered and fully rendered dataset
    '''
    OUTPUT_STABLE_DIR = os.path.join(OUTPUT_DIR, 'fullyrendered')
    if not os.path.isdir(OUTPUT_STABLE_DIR):
        os.mkdir(OUTPUT_STABLE_DIR)
    OUTPUT_UNSTABLE_DIR = os.path.join(OUTPUT_DIR, 'partiallyrendered')
    if not os.path.isdir(OUTPUT_UNSTABLE_DIR):
        os.mkdir(OUTPUT_UNSTABLE_DIR)

    for gif in tqdm.tqdm(glob.glob(os.path.join(ANIMATION_FOLDER, '*/*/gifs/*.gif'))):
        vs = VideoScene(gif, STABLE_DURATION, STALE_THRESHOLD, NUM_UNSTABLE,
                            GESTURE_FOLDER, OUTPUT_STABLE_DIR, OUTPUT_UNSTABLE_DIR)
        vs.write_dataset()
        

    print('Fully rendered:', len(glob.glob(f'{OUTPUT_STABLE_DIR}/*.jpg')))
    print('Partially rendered:', len(glob.glob(f'{OUTPUT_UNSTABLE_DIR}/*.jpg')))


    '''
        Split in training, validation, testing dataset
    '''
    split_dataset(OUTPUT_STABLE_DIR, OUTPUT_UNSTABLE_DIR, OUTPUT_DIR)




if __name__ == "__main__":
    main()