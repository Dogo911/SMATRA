#!/bin/bash

# Optional: kurz warten (z. B. bis Kamera oder X11 bereit)
sleep 10

# Starte die Objekterkennung im Container
python3 /opt/jetson-inference/python/training/detection/ssd/models/detectnet_mod.py \
  --model=/opt/jetson-inference/python/training/detection/ssd/models/TrCa30_OWN10/ssd-mobilenet.onnx \
  --labels=/opt/jetson-inference/python/training/detection/ssd/models/TrCa30_OWN10/labels.txt \
  --input-blob=input_0 \
  --output-cvg=scores \
  --output-bbox=boxes \
  csi://0

