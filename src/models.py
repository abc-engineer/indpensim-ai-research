import torch
import torch.nn as nn


class LSTMEncoder(nn.Module):
    def __init__(self, n_features: int, hidden_dim: int, latent_dim: int, n_layers: int = 1):
        super().__init__()
        self.lstm = nn.LSTM(n_features, hidden_dim, n_layers, batch_first=True)
        self.fc   = nn.Linear(hidden_dim, latent_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        _, (h, _) = self.lstm(x)
        return self.fc(h[-1])


class LSTMDecoder(nn.Module):
    def __init__(self, latent_dim: int, hidden_dim: int, n_features: int,
                 seq_len: int, n_layers: int = 1):
        super().__init__()
        self.seq_len = seq_len
        self.fc      = nn.Linear(latent_dim, hidden_dim)
        self.lstm    = nn.LSTM(hidden_dim, hidden_dim, n_layers, batch_first=True)
        self.out     = nn.Linear(hidden_dim, n_features)

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        h   = self.fc(z).unsqueeze(1).repeat(1, self.seq_len, 1)
        out, _ = self.lstm(h)
        return self.out(out)


class LSTMAutoencoder(nn.Module):
    def __init__(self, n_features: int, hidden_dim: int = 64, latent_dim: int = 32,
                 seq_len: int = 50, n_layers: int = 1):
        super().__init__()
        self.encoder = LSTMEncoder(n_features, hidden_dim, latent_dim, n_layers)
        self.decoder = LSTMDecoder(latent_dim, hidden_dim, n_features, seq_len, n_layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        z = self.encoder(x)
        return self.decoder(z)
