#!/bin/bash

cd ~/jetson-inference_2.0 || exit 1

# Starte den Container und führe direkt das Python-Skript aus
./docker/run.sh 
sleep 15
python3 /opt/jetson-inference/python/training/detection/ssd/models/detectnet_mod.py \
  --model=/opt/jetson-inference/python/training/detection/ssd/models/TrCa30_OWN10/ssd-mobilenet.onnx \
  --labels=/opt/jetson-inference/python/training/detection/ssd/models/TrCa30_OWN10/labels.txt \
  --input-blob=input_0 \
  --output-cvg=scores \
  --output-bbox=boxes \
  csi://0

