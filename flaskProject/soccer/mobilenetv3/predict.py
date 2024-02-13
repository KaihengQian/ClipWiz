import os
import json
import cv2

import torch
from PIL import Image
from torchvision import transforms

from model_v3 import mobilenet_v3_large


def predict(frame):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    data_transform = transforms.Compose(
        [transforms.Resize(256),
         transforms.CenterCrop(224),
         transforms.ToTensor(),
         transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

    # transform image format
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb)
    # [N, C, H, W]
    img = data_transform(img)
    # expand batch dimension
    img = torch.unsqueeze(img, dim=0)
    # read class_indict
    json_path = 'class_indices.json'
    assert os.path.exists(json_path), "file: '{}' dose not exist.".format(json_path)

    with open(json_path, "r") as f:
        class_indict = json.load(f)

    # create model
    model = mobilenet_v3_large(num_classes=8).to(device)
    # load model weights
    model_weight_path = "trained_model.pth"
    model.load_state_dict(torch.load(model_weight_path, map_location=device))
    model.eval()
    with torch.no_grad():
        # predict class
        output = torch.squeeze(model(img.to(device))).cpu()
        predict = torch.softmax(output, dim=0)
        # predict_cla = torch.argmax(predict).numpy()

    max_prob, max_prob_index = torch.max(predict, dim=0)
    max_prob_class = class_indict[str(max_prob_index.item())]

    return max_prob_class
