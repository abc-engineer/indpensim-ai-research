import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.metrics import roc_auc_score, average_precision_score, roc_curve


def train(model: nn.Module, windows: np.ndarray, config: dict, device: str = 'cpu') -> list:
    model = model.to(device)
    X      = torch.tensor(windows, dtype=torch.float32)
    loader = DataLoader(TensorDataset(X), batch_size=config['batch_size'], shuffle=True)
    optimizer = torch.optim.Adam(model.parameters(), lr=config['lr'])
    criterion = nn.MSELoss()

    history = []
    model.train()
    for epoch in range(config['epochs']):
        epoch_loss = 0.0
        for (batch,) in loader:
            batch = batch.to(device)
            recon = model(batch)
            loss  = criterion(recon, batch)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
        avg = epoch_loss / len(loader)
        history.append(avg)
        if (epoch + 1) % 10 == 0:
            print(f'Epoch [{epoch+1:3d}/{config["epochs"]}]  Loss: {avg:.6f}')

    return history


def batch_anomaly_score(model: nn.Module, sequence: np.ndarray,
                        window_size: int, stride: int, device: str = 'cpu') -> float:
    model.eval()
    criterion = nn.MSELoss(reduction='none')
    scores = []

    with torch.no_grad():
        for start in range(0, len(sequence) - window_size + 1, stride):
            w     = torch.tensor(sequence[start:start + window_size],
                                 dtype=torch.float32).unsqueeze(0).to(device)
            recon = model(w)
            scores.append(criterion(recon, w).mean().item())

    return float(np.mean(scores)) if scores else 0.0


def evaluate(model: nn.Module, X_test: list, y_test: list,
             window_size: int, stride: int, device: str = 'cpu') -> dict:
    scores = [batch_anomaly_score(model, seq, window_size, stride, device) for seq in X_test]
    auroc  = roc_auc_score(y_test, scores)
    auprc  = average_precision_score(y_test, scores)
    fpr, tpr, thresholds = roc_curve(y_test, scores)

    return {
        'scores':     scores,
        'auroc':      auroc,
        'auprc':      auprc,
        'fpr':        fpr,
        'tpr':        tpr,
        'thresholds': thresholds,
    }


def find_threshold(scores: list, y_true: list, percentile: float = 95) -> float:
    normal_scores = [s for s, y in zip(scores, y_true) if y == 0]
    return float(np.percentile(normal_scores, percentile))
