#!/bin/bash

gnome-terminal -- bash -c "
cd /home/smarttraversejetson/jetson-inference_2.0 || { echo 'Ordner jetson-inference_2.0 nicht gefunden!'; exit 1; }

sudo ./docker/run.sh --run python3 /opt/jetson-inference/python/training/detection/ssd/models/detectnet_mod.py \
  --model=/opt/jetson-inference/python/training/detection/ssd/models/TrCa30_OWN10/ssd-mobilenet.onnx \
  --labels=/opt/jetson-inference/python/training/detection/ssd/models/TrCa30_OWN10/labels.txt \
  --input-blob=input_0 --output-cvg=scores --output-bbox=boxes \
  csi://1

exec bash"
