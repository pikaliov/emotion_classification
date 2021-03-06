from torch.nn import Module, LSTM, Linear
from torch.nn.functional import relu
from torch import cat


class BidirectionalLSTM(Module):
    """
    Model is based on model found in paper: Emotion Recognition From Speech With Recurrent Neural Networks.
    My GPU cannot handle the full model however so I have cut down on some of the parameters.
    """

    def __init__(self, model_configs):
        super(BidirectionalLSTM, self).__init__()

        self.configs = model_configs
        self.lstm_1 = LSTM(input_size=1, hidden_size=self.configs.lstm_output_dim,
                           num_layers=self.configs.lstm_layers, batch_first=False, dropout=1, bidirectional=True)
        self.dense_2 = Linear(in_features=2 * self.configs.lstm_output_dim,
                              out_features=self.configs.dense_1_output_dim)
        self.dense_3 = Linear(in_features=self.configs.dense_1_output_dim, out_features=self.configs.dense_2_output_dim)

    def forward(self, x):
        x = x.view(self.configs.batch_size, -1, 1)
        x, hidden = self.lstm_1(x)

        y = None
        for i in range(0, self.configs.batch_size):
            y_prime = cat([x[i,0,0:self.configs.lstm_output_dim], x[i,-1,self.configs.lstm_output_dim:]])
            y_prime = y_prime.view(1, -1)
            if i == 0:
                y = y_prime
            else:
                y = cat([y, y_prime], dim=0)

        x = relu(self.dense_2(y))
        x = self.dense_3(x)
        return x
