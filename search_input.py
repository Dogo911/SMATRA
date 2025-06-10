import onnx

model = onnx.load("/home/smarttraversejetson/jetson-inference/build/aarch64/bin/networks/ssd_mob_onnx/ssd_mobilenet_v1_10.onnx")
print("Model Inputs:")
for input_tensor in model.graph.input:
    print(" -", input_tensor.name)
