# Machine learning baselines
OUTPUT_DIR="model_sift_svm"
DATA_PATH="binaryUI_app"
IMG_FEATURE="sift"
CLASSIFER="svm"

mkdir "$OUTPUT_DIR"

python train.py --output_dir ${OUTPUT_DIR} \
                 --do_train \
                 --img_feature ${IMG_FEATURE} \
                 --classifer ${CLASSIFER} \
                 --data_path ${DATA_PATH}
