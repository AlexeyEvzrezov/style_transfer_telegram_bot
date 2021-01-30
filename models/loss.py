from abc import ABC

import torch.nn.functional as F
from torch import nn


class NSTLoss(nn.Module, ABC):

    def __init__(self, model, content_img, style_img,
                 content_layers=None, style_layers=None,
                 content_weights=None, style_weights=None,
                 alpha=1, beta=1e4):
        super(NSTLoss, self).__init__()
        self.model = model
        if content_layers is None:
            content_layers = [22]
        if style_layers is None:
            style_layers = [1, 6, 11, 20, 29]
        if content_weights is None:
            len_layers = len(content_layers)
            self.content_weights = [1. / len_layers] * len_layers
        else:
            self.content_weights = content_weights
        if style_weights is None:
            len_layers = len(style_layers)
            self.style_weights = [1. / len_layers] * len_layers
        else:
            self.style_weights = style_weights
        self.content_activations_lst = model(content_img, content_layers)
        self.style_activations_lst = model(style_img, style_layers)
        self.loss_layers = sorted(set(content_layers + style_layers))
        self.content_ids = [self.loss_layers.index(i) for i in content_layers]
        self.style_ids = [self.loss_layers.index(i) for i in style_layers]
        self.alpha = alpha
        self.beta = beta

    def content_loss(self, target, inp):
        return 1 / 2. * F.mse_loss(target, inp)

    def style_loss(self, target, inp):
        target_gram = self.gram_matrix(target)
        input_gram = self.gram_matrix(inp)
        return F.mse_loss(target_gram, input_gram)

    def gram_matrix(self, inp):
        (b, ch, h, w) = inp.size()
        features = inp.view(b, ch, h * w)
        G = features.bmm(features.transpose(1, 2))
        return G / (2 * ch * h * w)

    def loss_weight_sum(self, loss_fn, inp, activations_lst, weights_lst):
        loss_sum = 0
        for idx, x in enumerate(activations_lst):
            loss_sum += loss_fn(x, inp[idx]) * weights_lst[idx]
        return loss_sum

    def forward(self, inp):
        input_lst = self.model(inp, self.loss_layers)
        input_content_lst = [input_lst[i] for i in self.content_ids]
        input_style_lst = [input_lst[i] for i in self.style_ids]
        weighted_content_losses = self.loss_weight_sum(
            self.content_loss, input_content_lst,
            self.content_activations_lst, self.content_weights)
        weighted_style_losses = self.loss_weight_sum(
            self.style_loss, input_style_lst,
            self.style_activations_lst, self.style_weights)

        total_loss = (self.alpha * weighted_content_losses +
                      self.beta * weighted_style_losses)

        return total_loss
