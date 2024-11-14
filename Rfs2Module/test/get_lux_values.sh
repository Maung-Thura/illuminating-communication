python3 -m pip install azure-iot-device smbus2
cd /home/root/Rfs2Module/test
while true; do
    python3 suite_test.py 2> /dev/null | grep '"lux"' | sed -E 's/. *"lux": ([0-9.]+). */\1/'
done