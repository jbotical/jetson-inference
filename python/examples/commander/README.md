

# Run locally with local camera

# (This is not using a container)

```
NET=/home/elephant/repos/jetson-inference/python/training/detection/ssd/models/test2;OPENBLAS_CORETYPE=ARMV8 ./detectnet-new-object.py --model=$NET/ssd-mobilenet.onnx --labels=$NET/labels.txt --input-blob=input_0 --output-cvg=scores --output-bbox=boxes /dev/video0 
```
