from abc import ABC

from torch import nn


class NST(nn.Module, ABC):

    def __init__(self, model):
        super(NST, self).__init__()
        self.model = model
        for param in self.model.parameters():
            param.requires_grad = False

    def forward(self, x, loss_layers):
        ongoing_layer = 0
        loss_layers.sort()

        activations = x.clone()
        activations_lst = []

        for i in loss_layers:
            layer = self.model[ongoing_layer:i + 1]
            activations = layer(activations)
            activations_lst.append(activations)
            ongoing_layer = i + 1

        return activations_lst
