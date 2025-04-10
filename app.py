from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
from keras.models import Sequential # type: ignore
from keras.layers import Dense # type: ignore

app = Flask(__name__)

def ann():
    model = Sequential()
    model.add(Dense(30, input_dim=32, activation='relu', kernel_initializer='random_uniform'))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(5, activation='softmax'))
    model.compile(loss="categorical_crossentropy", optimizer='adam', metrics=['accuracy'])
    return model

import __main__
__main__.ann = ann 

try:
    scaler = joblib.load('models/scaler.joblib')
    model_ann = joblib.load('models/model_ann.joblib')
    label_encoder = joblib.load('models/label_encoder.joblib')
except Exception as e:
    print("Model loading error:", str(e))
    raise

@app.route('/')
def home():
    return "Welcome to the Intrusion Detection System API!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 1. Verify that the request is JSON
        if not request.is_json:
            return jsonify({"error": "Requête non-JSON", "status": "failed"}), 400
            
        data = request.get_json()
        
        # 2. Transformation in DataFrame
        required_features = ['protocol_type', 'flag', 'src_bytes', 'dst_bytes', "land", "wrong_fragment", "urgent", "hot", 
                             "num_failed_logins", "logged_in", "num_compromised", "root_shell", "su_attempted", "num_file_creations", 
                             "num_shells", "num_access_files", "is_guest_login", "count", "srv_count", "serror_rate", "rerror_rate", 
                             "same_srv_rate", "diff_srv_rate", "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count", 
                             "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate", 
                             "dst_host_srv_diff_host_rate", "time"]

        for feat in required_features:
            if feat not in data:
                return jsonify({"error": f"Feature manquante: {feat}", "status": "failed"}), 400
                
        input_df = pd.DataFrame([data])

        # 3. Preprocessing
        pmap = {'icmp':0, 'tcp':1, 'udp':2}
        fmap = {'SF':0, 'S0':1, 'REJ':2, 'RSTR':3, 'RSTO':4, 'SH':5, 'OTH':10}  # Adaptez
        input_df['protocol_type'] = input_df['protocol_type'].map(pmap)
        input_df['flag'] = input_df['flag'].map(fmap)
        input_df.drop(['service', 'target'], axis=1, errors='ignore', inplace=True)

        # 4. Dimension check
        if input_df.shape[1] != 32:
            return jsonify({
                "error": f"Nombre de features incorrect (reçu: {input_df.shape[1]}, attendu: 32)",
                "status": "failed"
            }), 400

        # 5. Prediction
        X = scaler.transform(input_df)
        ann_proba = model_ann.predict_proba(X) # this is the confidence of the model 
        ann_pred = label_encoder.inverse_transform([np.argmax(ann_proba)])[0] # this is the predicted class (normal, dos, probe, r2l or u2r)

        return jsonify({
            "prediction": str(ann_pred),
            "confidence": float(np.max(ann_proba)),
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "error": f"Erreur interne: {str(e)}",
            "status": "failed"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)