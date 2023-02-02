SEED_DIR="./seed_dir"
THEMIS_DIR="./themis"
SERIAL="emulator-5556"
OUTPUT_DIR="./output_throttle_200"
THROTTLE="200"
REPLAY_MODE="touch"

rm -r ${OUTPUT_DIR}
mkdir ${OUTPUT_DIR}

python replay.py --seed_dir ${SEED_DIR} \
                --themis_dir ${THEMIS_DIR} \
                --device_serial ${SERIAL} \
                --output_dir ${OUTPUT_DIR} \
                --throttle ${THROTTLE} \
                --replay_mode ${REPLAY_MODE} \
                --use_classifer \
                --use_minicap