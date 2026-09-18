import pandas as pd
import os
import warnings
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
from alerts.alert_manager import create_alert

# Suppress sklearn warnings about feature names
warnings.filterwarnings("ignore", category=UserWarning)

class NetworkMLDetector:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.model = IsolationForest(contamination=0.05, random_state=42)
        self.encoder = LabelEncoder()
        self.is_trained = False
        
        self._train_model()

    def _train_model(self):
        if not os.path.exists(self.csv_file_path):
            print("\n[ML] No historical data found. AI is dormant.")
            return

        try:
            df = pd.read_csv(self.csv_file_path)
            df = df.dropna()
            
            # Require at least 50 packets to form a decent baseline
            if len(df) < 50:
                print(f"\n[ML] Not enough data to train AI ({len(df)}/50 packets). Gathering more data...")
                return

            print(f"\n[ML] Training AI model on {len(df)} historical packets...")
            
            # Fit encoder and model
            df["Protocol_Encoded"] = self.encoder.fit_transform(df["Protocol"].astype(str))
            
            features = df[["Protocol_Encoded", "Packet_Size"]]
            self.model.fit(features.values) # using .values to avoid warning when predicting with feature names later
            
            self.is_trained = True
            print("[ML] AI Model successfully trained and ACTIVE!\n")
            
        except Exception as e:
            print(f"\n[ML] Error training model: {e}")
            self.is_trained = False

    def predict_packet(self, source_ip, destination_ip, protocol, source_port, destination_port, packet_size):
        if not self.is_trained:
            return

        try:
            # Try to encode the protocol
            protocol_encoded = self.encoder.transform([str(protocol)])[0]
        except ValueError:
            # Unseen protocol
            protocol_encoded = -1
        
        # Predict: 1 = Normal, -1 = Anomaly
        prediction = self.model.predict([[protocol_encoded, packet_size]])[0]
        
        if prediction == -1:
            create_alert(
                alert_type="AI Detected Anomaly",
                severity="HIGH",
                source_ip=source_ip,
                description=f"Isolation Forest flagged packet (Protocol: {protocol}, Size: {packet_size}) as anomalous behavior.",
                packet_size=packet_size,
                protocol=protocol,
                destination_port=destination_port
            )