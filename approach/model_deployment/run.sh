APK_PATH="test.apk"
SERIAL="emulator-5556"
OUTPUT_DIR="screenshots"

rm -r ${OUTPUT_DIR}
mkdir ${OUTPUT_DIR}

python start.py --apk ${APK_PATH} \
                --device_serial ${SERIAL} \
                --output_dir ${OUTPUT_DIR}