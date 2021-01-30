import torch
from torch import optim
from torchvision import models

from models.loss import NSTLoss
from models.nst import NST
from utils.imtransforms import str_to_tensor, tensor_to_str


def run_nst(content_img, style_img, img_size=256, max_iter=10):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    content_img = str_to_tensor(content_img, img_size).to(device)
    style_img = str_to_tensor(style_img, img_size).to(device)
    input_img = content_img.clone()
    vgg = models.vgg19(pretrained=True).features.to(device)
    model = NST(vgg).to(device)
    criterion = NSTLoss(model, content_img, style_img)
    optimizer = optim.LBFGS([input_img.requires_grad_()])

    n_iter = [0]
    while n_iter[0] <= max_iter:
        def closure():
            optimizer.zero_grad()
            loss = criterion(input_img)
            loss.backward()
            n_iter[0] += 1
            return loss
        optimizer.step(closure)

    return tensor_to_str(input_img)

