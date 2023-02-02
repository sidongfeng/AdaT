APK_FOLDER='apks'
OUTPUT_DIR='tf_apps_output_1'
DEVICE='device'

# automated explore apk
python apk_explore.py --apk_folder $APK_FOLDER \
                        --output_dir $OUTPUT_DIR \
                        --timeout 300 \
                        --interval 0.2 \
                        --d $DEVICE

# execute single apk
# adb -s DEVICE shell CLASSPATH=/data/local/tmp/ape.jar /system/bin/app_process /data/local/tmp/ com.android.commands.monkey.Monkey -p a2dp.Vol --running-minutes 3 --ape sata --throttle 1000