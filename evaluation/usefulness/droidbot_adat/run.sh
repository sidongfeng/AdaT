OUTPUT_DIR="output"
APK_FILE="a2dp.Vol_169.apk"
EMULATOR="emulator-5556"

mkdir "$OUTPUT_DIR"

droidbot-ours -a ${APK_FILE} \
         -o ${OUTPUT_DIR} \
         -d ${EMULATOR} \
         -timeout 240 > "${OUTPUT_DIR}/log.txt"
