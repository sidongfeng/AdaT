import cv2
import os
import sys
import glob
import tqdm
import time
import pickle
import argparse
import random
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
import sklearn
from sklearn.metrics import classification_report

from util import get_logger

global logger

def get_args(description='Experiments of machine learning based GUI rendering classification'):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--do_train", action='store_true', help="Whether to run training.")
    parser.add_argument("--do_eval", action='store_true', help="Whether to run eval on the dev set.")

    parser.add_argument('--data_path', type=str, default='data',
                        help='image file path')
    parser.add_argument('--img_feature', type=str, default='sift',
                        help='image feature extractor')
    parser.add_argument('--classifer', type=str, default='svm',
                        help='feature classifer')
    parser.add_argument('--n_sample', type=int, default=20, help='downsample feature descriptors')
    parser.add_argument('--vocab_size', type=int, default=200, help='vocabulary size for BoW')
    parser.add_argument('--seed', type=int, default=42, help='random seed')

    parser.add_argument("--output_dir", default=None, type=str, required=True,
                        help="The output directory where the model predictions and checkpoints will be written.")
    parser.add_argument("--init_model", default=None, type=str, required=False, help="Initial model.")
    args = parser.parse_args()

    # Check paramenters
    if not args.do_train and not args.do_eval:
        raise ValueError("At least one of `do_train` or `do_eval` must be True.")

    # Check paramenters
    if args.do_eval and args.init_model is None:
        raise ValueError("`do_eval` must be have initial model.")


    return args

def set_seed_logger(args):
    global logger
    # predefining random initial seeds
    random.seed(args.seed)
    np.random.seed(args.seed)

    logger = get_logger(os.path.join(args.output_dir, "log.log"))

    logger.info("Effective parameters:")
    for key in sorted(args.__dict__):
        logger.info("  <<< {}: {}".format(key, args.__dict__[key]))

    return args

def init_model(args):
    if args.classifer == 'svm':
        model = sklearn.svm.SVC(random_state=args.seed)
    elif args.classifer == 'knn':
        model = sklearn.neighbors.KNeighborsClassifier()
    elif args.classifer == 'nb':
        model = GaussianNB()
    elif args.classifer == 'rf':
        model = RandomForestClassifier(max_depth=2, random_state=args.seed)
    return model

def imgFeatures(img, args):
    if args.img_feature == 'sift':
        sift = cv2.xfeatures2d.SIFT_create()
        _, des = sift.detectAndCompute(img, None)
    elif args.img_feature == 'surf':
        surf = cv2.xfeatures2d.SURF_create()
        _, des = surf.detectAndCompute(img, None)
    elif args.img_feature == 'orb':
        orb = cv2.ORB_create(nfeatures=1500)
        _, des = orb.detectAndCompute(img, None)
    if des is not None:
        des = des[np.random.randint(des.shape[0], size=args.n_sample)]
    return des

def load_dataset(dir, args):
    features = []
    labels = []
    img_paths = glob.glob(dir)
    random.shuffle(img_paths)
    for img_path in tqdm.tqdm(img_paths):
        img = cv2.imread(img_path, 0)
        if img is None:
            continue
        img_des = imgFeatures(img, args)
        if img_des is None:
            continue
        features.append(img_des)
        tag = img_path.split('/')[-2]
        labels.append(tag)
    return features, labels

def load_voc_feature(feature, kmeans, args):
    voc_features = []
    for feat in tqdm.tqdm(feature):
        distance = cdist(feat, kmeans, 'euclidean')
        bin_assignment = np.argmin(distance, axis=1)
        voc_feat = np.zeros(args.vocab_size)
        for id_assign in bin_assignment:
            voc_feat[id_assign] += 1
        voc_features.append(voc_feat)
    return voc_features


def main():
    global logger
    args = get_args()
    args = set_seed_logger(args)
    model = init_model(args)

    # Train the model
    train_dir = os.path.join(args.data_path, 'train', '*', '*.jpg')
    train_features, train_labels = load_dataset(train_dir, args)

    kmeans = KMeans(n_clusters=args.vocab_size, random_state=args.seed) \
                    .fit(np.vstack(train_features)).cluster_centers_
    
    if args.do_train:
        train_voc_features = load_voc_feature(train_features, kmeans, args)
        model.fit(train_voc_features, train_labels)
        logger.info(f" >>> Training accuracy: {model.score(train_voc_features, train_labels)}")
        
        filename = os.path.join(args.output_dir, f'model_{args.img_feature}_{args.classifer}.sav')
        pickle.dump(model, open(filename, 'wb'))

    # Test the model
    test_dir = os.path.join(args.data_path, 'val', '*', '*.jpg')
    test_features, test_labels = load_dataset(test_dir, args)
    test_voc_features = load_voc_feature(test_features, kmeans, args)

    if args.init_model is not None:
        model = pickle.load(open(args.init_model, 'rb'))

    start_time = time.time()
    test_pred = model.predict(test_voc_features)
    report = classification_report(test_labels, test_pred)
    logger.info(" >>> Testing report:")
    logger.info(report)
    logger.info(f" >>> Inference time: {(time.time()-start_time)/len(test_labels)}")

if __name__ == "__main__":
    main()
