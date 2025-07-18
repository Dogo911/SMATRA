!/usr/bin/env python3
#
# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#

import sys
import argparse
import requests
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput, Log

# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object>
                                 formatter_class=argparse.RawTextHelpFormatter, 
                                 epilog=detectNet.Usage() + videoSource.Usage() + videoOutput.Usage(>

parser.add_argument("input", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to lo>
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags >
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use>

try:
        args = parser.parse_known_args()[0]
except:
        print("")
        parser.print_help()
        sys.exit(0)

# create video sources and outputs
input = videoSource(args.input, argv=sys.argv)
output = videoOutput(args.output, argv=sys.argv)

# load the object detection network
net = detectNet(args.network, sys.argv, args.threshold)

# note: to hard-code the paths to load a model, the following API can be used:
#
# net = detectNet(model="model/ssd-mobilenet.onnx", labels="model/labels.txt", 
#                 input_blob="input_0", output_cvg="scores", output_bbox="boxes", 

#                 input_blob="input_0", output_cvg="scores", output_bbox="boxes", 
#                 threshold=args.threshold)

# process frames until EOS or the user exits
while True:
    # capture the next image
    img = input.Capture()

    if img is None: # timeout
        continue  

    # detect objects in the image (with overlay)
    detections = net.Detect(img, overlay=args.overlay)

    # print the detections
    print("detected {:d} objects in image".format(len(detections)))

    for detection in detections:
        print(detection)
        class_id = detection.ClassID
        class_name = net.GetClassDesc(class_id)
        print("ID: ", class_id)
        print("ID:", detection.ClassID)
        print("Name: ", class_name)

# HTTP POST an Raspberry Pi senden
        if class_name == "Truck":
           icon = "truck"
           limit = "80"
        else:
           icon = "car"
           limit = "120"
        try:
            payload = {
                "velocity": limit,
                "speed": "",
                "icon": icon
            }
            response = requests.post("http://192.168.0.60:5000/update", json=payload)
            if response.status_code == 200:
                print("Daten erfolgreich gesendet.")
            else:
                print(f"Fehler beim Senden: {response.status_code}")
        except Exception as e:
             print(f"Fehler beim HTTP-POST: {e}")
    # render the image
    output.Render(img)

    # update the title bar
    output.SetStatus("{:s} | Network {:.0f} FPS".format(args.network, net.GetNetworkFPS()))

    # print out performance info
    net.PrintProfilerTimes()

    # exit on input/output EOS
    if not input.IsStreaming() or not output.IsStreaming():
while True:
    # capture the next image
    img = input.Capture()

    if img is None: # timeout
        continue  

    # detect objects in the image (with overlay)
    detections = net.Detect(img, overlay=args.overlay)

    # print the detections
    print("detected {:d} objects in image".format(len(detections)))

    for detection in detections:
        print(detection)
        class_id = detection.ClassID
        class_name = net.GetClassDesc(class_id)
        print("ID: ", class_id)
        print("ID:", detection.ClassID)
        print("Name: ", class_name)

# HTTP POST an Raspberry Pi senden
        if class_name == "Truck":
           icon = "truck"
           limit = "80"
        else:
           icon = "car"
           limit = "120"
        try:
            payload = {
                "velocity": limit,
                "speed": "",
                "icon": icon
            }
            response = requests.post("http://192.168.0.60:5000/update", json=payload)
            if response.status_code == 200:
                print("Daten erfolgreich gesendet.")
            else:
                print(f"Fehler beim Senden: {response.status_code}")
        except Exception as e:
             print(f"Fehler beim HTTP-POST: {e}")
    # render the image
    output.Render(img)

    # update the title bar
    output.SetStatus("{:s} | Network {:.0f} FPS".format(args.network, net.GetNetworkFPS()))

    # print out performance info
    net.PrintProfilerTimes()

    # exit on input/output EOS
    if not input.IsStreaming() or not output.IsStreaming():
        break




