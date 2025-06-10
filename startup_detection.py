#!/bin/bash

gnome-terminal -- bash -c '
cd /home/smarttraversejetson/jetson-inference_2.0 &&
echo "🔐 Starte Docker-Container..." &&
echo "smatra1234" | sudo -S bash docker/run.sh &&
echo "⏳ Warte 5 Sekunden..." &&
sleep 5 &&
echo "🚀 Starte Objekterkennung..." &&
docker exec -it jetson-inference bash -c "
python3 /opt/jetson-inference/python/training/detection/ssd/models/detectnet_mod.py \
--model=/opt/jetson-inference/python/training/detection/ssd/models/TrCa30_OWN10/ssd-mobilenet.onnx \
--labels=/opt/jetson-inference/python/training/detection/ssd/models/TrCa30_OWN10/labels.txt \
--input-blob=input_0 --output-cvg=scores --output-bbox=boxes csi://0
"; exec bash'

