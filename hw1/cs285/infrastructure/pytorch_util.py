from typing import Union

import torch
from torch import nn

Activation = Union[str, nn.Module]


_str_to_activation = {
    'relu': nn.ReLU(),
    'tanh': nn.Tanh(),
    'leaky_relu': nn.LeakyReLU(),
    'sigmoid': nn.Sigmoid(),
    'selu': nn.SELU(),
    'softplus': nn.Softplus(),
    'identity': nn.Identity(),
}


class MLP(nn.Module):
  def __init__(self,
               input_size,
               output_size,
               n_layers,
               size,
               activation,
               output_activation):
    super(MLP, self).__init__()
    self.layers = []
    i = 0
    while(i != n_layers + 1): # Input Layer + n_layers hidden layers
      if i == 0:
        self.layers.append(nn.Linear(input_size, size))
      else:
        self.hidden.append(activation)
        self.hidden.append(nn.Linear(size, size))
      i += 1
    self.layers = nn.Sequential(*self.layers)
    self.output_logits = output_activation

  def forward(self, x):
    x = x.flatten()
    x = self.layers(x)
    logits = self.output_logits(x)
    return logits
    

def build_mlp(
        input_size: int,
        output_size: int,
        n_layers: int,
        size: int,
        activation: Activation = 'tanh',
        output_activation: Activation = 'identity',
) -> nn.Module:
    """
        Builds a feedforward neural network

        arguments:
            n_layers: number of hidden layers
            size: dimension of each hidden layer
            activation: activation of each hidden layer

            input_size: size of the input layer
            output_size: size of the output layer
            output_activation: activation of the output layer

        returns:
            MLP (nn.Module)
    """
    if isinstance(activation, str):
        activation = _str_to_activation[activation]
    if isinstance(output_activation, str):
        output_activation = _str_to_activation[output_activation]

    model = MLP(input_size, output_size, n_layers, size, activation, output_activation)
    return model


device = None


def init_gpu(use_gpu=True, gpu_id=0):
    global device
    if torch.cuda.is_available() and use_gpu:
        device = torch.device("cuda:" + str(gpu_id))
        print("Using GPU id {}".format(gpu_id))
    else:
        device = torch.device("cpu")
        print("GPU not detected. Defaulting to CPU.")


def set_device(gpu_id):
    torch.cuda.set_device(gpu_id)


def from_numpy(*args, **kwargs):
    return torch.from_numpy(*args, **kwargs).float().to(device)


def to_numpy(tensor):
    return tensor.to('cpu').detach().numpy()
