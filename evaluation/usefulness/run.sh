# droidbot
APK_FOLDER='select_apks'
OUTPUT_DIR='origin_10min_throttle_200ms'
DEVICE='emulator-5556'
TIMEOUT="600"
INTERVAL="0.2"

rm -r ${OUTPUT_DIR}
mkdir ${OUTPUT_DIR}

python apk_explore.py --apk_folder $APK_FOLDER \
                            --output_dir $OUTPUT_DIR \
                            --timeout $TIMEOUT \
                            --interval $INTERVAL \
                            --d $DEVICE


# get activities
APK_FOLDER='select_apks'
OUTPUT_DIR='activities'
DEVICE='emulator-5556'

rm -r ${OUTPUT_DIR}
mkdir ${OUTPUT_DIR}

python get_activities.py --apk_folder $APK_FOLDER \
                            --output_dir $OUTPUT_DIR \
                            --d $DEVICE