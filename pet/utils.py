import io
import torchvision.transforms as transforms
import base64
import datetime
from torchvision import models
from PIL import Image
import json

imagenet_class_index = json.load(open('pet/static/imagenet_class_index.json'))

model = models.resnet34(weights='ResNet34_Weights.DEFAULT')
model.eval()


def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize(255),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)


def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    return imagenet_class_index[predicted_idx]


def get_result(image_file,is_api = False):
    start_time = datetime.datetime.now()
    image_bytes = image_file.file.read()
    class_id,class_name = get_prediction(image_bytes)
    end_time = datetime.datetime.now()
    time_diff = (end_time - start_time)
    execution_time = f'{round(time_diff.total_seconds() * 1000)} ms'
    encoded_string = base64.b64encode(image_bytes)
    bs64 = encoded_string.decode('utf-8')
    image_data = f'data:image/jpeg;base64,{bs64}'   
    result = {
        "inference_time":execution_time,
        "predictions":{
            "class_id":class_id,
            "class_name":class_name
        }
    }
    if not is_api: 
        result["image_data"]= image_data
    return result