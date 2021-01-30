import numpy as np
import torch
from PIL import Image
import io
import torchvision.transforms as transforms


def str_to_tensor(img_str, size=None):
    buf = io.BytesIO(img_str)
    img_pil = Image.open(buf)
    transform = transforms.Compose([
        transforms.Resize(size),
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x[torch.LongTensor([2, 1, 0])]),
        transforms.Normalize((0.406, 0.456, 0.485), (1, 1, 1)),
        transforms.Lambda(lambda x: x.mul_(255)),
        ])
    return transform(img_pil).unsqueeze(0)


def tensor_to_str(img_tensor):
    transform = transforms.Compose([
        transforms.Lambda(lambda x: x.mul_(1./255)),
        transforms.Normalize((-0.406, -0.456, -0.485), (1, 1, 1)),
        transforms.Lambda(lambda x: x[torch.LongTensor([2, 1, 0])]),
        ])
    img_tensor = transform(img_tensor.cpu().squeeze())
    img_tensor = img_tensor.clamp(0, 1)
    img_pil = transforms.ToPILImage()(img_tensor)
    # img_pil = Image.fromarray((img_np * 255).astype(np.uint8))
    buf = io.BytesIO()
    img_pil.save(buf, format='JPEG')
    img_str = buf.getvalue()
    return img_str


# def imload(img_str):
#     img_pil = Image.open(io.BytesIO(img_str))
#     img_pil = show(load_img(img_pil))
#     img_pil = Image.fromarray((img_pil * 255).astype(np.uint8))
#     buf = io.BytesIO()
#     img_pil.save(buf, format='JPEG')
#     byte_im = buf.getvalue()
#     return byte_im
#
# def load_img(img):
#
#     img = transforms.Resize((100, 100))(img)
#
#     transform = transforms.Compose([
#         transforms.ToTensor(),
#         transforms.Normalize((0.485, 0.456, 0.406),
#                              (0.229, 0.224, 0.225))
#     ])
#
#     return transform(img).unsqueeze(0)
#
#
# def show(x):
#     x = x.to('cpu').clone().detach()
#     x = x.numpy().squeeze(0)
#     x = x.transpose(1, 2, 0)
#     x = x * np.array((0.229, 0.224, 0.225)) + np.array((0.485, 0.456, 0.406))
#     x = x.clip(0, 1)
#     return x#.tobytes()

# from io import BytesIO
# bio = BytesIO()
# bio.name = 'image.jpeg'
# image.save(bio, 'JPEG')
# bio.seek(0)
# bot.send_photo(chat_id, photo=bio)