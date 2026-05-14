import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import StandardScaler

BATCH_COL       = 'Batch reference(Batch_ref:Batch ref)'
BATCH_COL_STATS = 'Batch ref'
FAULT_COL       = 'Fault ref(0-NoFault 1-Fault)'

# 실시간 측정 공정 변수 (오프라인/희소 변수 제외)
ONLINE_VARS = [
    'Aeration rate(Fg:L/h)',
    'Agitator RPM(RPM:RPM)',
    'Sugar feed rate(Fs:L/h)',
    'Acid flow rate(Fa:L/h)',
    'Base flow rate(Fb:L/h)',
    'Heating/cooling water flow rate(Fc:L/h)',
    'Heating water flow rate(Fh:L/h)',
    'Water for injection/dilution(Fw:L/h)',
    'Air head pressure(pressure:bar)',
    'Dumped broth flow(Fremoved:L/h)',
    'Substrate concentration(S:g/L)',
    'Dissolved oxygen concentration(DO2:mg/L)',
    'Penicillin concentration(P:g/L)',
    'Vessel Volume(V:L)',
    'Vessel Weight(Wt:Kg)',
    'pH(pH:pH)',
    'Temperature(T:K)',
    'Generated heat(Q:kJ)',
    'carbon dioxide percent in off-gas(CO2outgas:%)',
    'PAA flow(Fpaa:PAA flow (L/h))',
    'Oil flow(Foil:L/hr)',
    'Oxygen Uptake Rate(OUR:(g min^{-1}))',
    'Oxygen in percent in off-gas(O2:O2  (%))',
    'Carbon evolution rate(CER:g/h)',
]


def load_data(data_dir: str):
    data_dir = Path(data_dir)
    df = pd.read_csv(data_dir / '100_Batches_IndPenSim_V3.csv')
    df.columns = df.columns.str.strip()
    df_stats = pd.read_csv(data_dir / '100_Batches_IndPenSim_Statistics.csv')
    df_stats.columns = df_stats.columns.str.strip()
    return df, df_stats


def get_fault_labels(df_stats: pd.DataFrame) -> dict:
    return {int(k): int(v) for k, v in
            df_stats.set_index(BATCH_COL_STATS)[FAULT_COL].to_dict().items()}


def get_batch_sequences(df: pd.DataFrame, df_stats: pd.DataFrame, scaler=None):
    labels = get_fault_labels(df_stats)

    # NaN 제거 후 float → int 변환 (1.0 → 1)
    df = df.dropna(subset=[BATCH_COL]).copy()
    df[BATCH_COL] = df[BATCH_COL].astype(float).astype(int)

    # 두 파일에 공통으로 존재하는 배치 ID만 사용
    batch_ids = sorted(set(df[BATCH_COL].unique()) & set(labels.keys()))

    sequences = {
        bid: df[df[BATCH_COL] == bid][ONLINE_VARS].values.astype(np.float32)
        for bid in batch_ids
    }

    if scaler is None:
        normal_ids  = [bid for bid in batch_ids if labels[bid] == 0]
        normal_data = np.vstack([sequences[bid] for bid in normal_ids])
        scaler = StandardScaler().fit(normal_data)

    scaled = {bid: scaler.transform(seq) for bid, seq in sequences.items()}
    return scaled, labels, scaler


def train_test_split(sequences: dict, labels: dict):
    normal_ids = sorted([bid for bid, lbl in labels.items() if lbl == 0])
    all_ids    = sorted(labels.keys())

    X_train   = [sequences[bid] for bid in normal_ids]
    X_test    = [sequences[bid] for bid in all_ids]
    y_test    = [labels[bid]    for bid in all_ids]
    batch_ids = all_ids

    return X_train, X_test, y_test, batch_ids


def make_windows(sequences: list, window_size: int, stride: int) -> np.ndarray:
    windows = []
    for seq in sequences:
        for start in range(0, len(seq) - window_size + 1, stride):
            windows.append(seq[start:start + window_size])
    return np.array(windows, dtype=np.float32)
