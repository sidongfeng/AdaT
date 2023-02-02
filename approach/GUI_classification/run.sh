# Train model
OUTPUT_DIR=$(date +"%m-%d-%H.%M.%S")
DATA_PATH="/user-data/binaryUI_app"

mkdir "$OUTPUT_DIR"

python train.py --output_dir ${OUTPUT_DIR} \
                 --do_train \
                 --do_pretrain \
                 --epochs 20 \
                 --data_path ${DATA_PATH} \
                 --num_workers 8 \
                 --lr 0.0001 \
                 --model_name mobilenet \
                 --batch_size 64

# Test model
OUTPUT_DIR="test_model"
DATA_PATH="/dataset"
MODEL="output/mobilenet/pytorch_model.bin.20"
MODEL_NAME="mobilenet"

mkdir "$OUTPUT_DIR"

python train.py --output_dir ${OUTPUT_DIR} \
                 --do_eval \
                 --data_path ${DATA_PATH} \
                 --num_workers 8 \
                 --model_name ${MODEL_NAME} \
                 --init_model ${MODEL}


# Inference model
IMAGE_FOLDER="inference"
MODEL="output/mobilenet/pytorch_model.bin.20"
MODEL_NAME="mobilenet"

python inference.py --data_path ${IMAGE_FOLDER} \
                    --init_model ${MODEL} \
                    --model_name ${MODEL_NAME} 
