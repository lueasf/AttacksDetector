import requests
import json

url_docker = "http://localhost:8080/predict"

payload = {
    "duration": 0,
    "protocol_type": "tcp",    # will be maped to 1
    "flag": "SF",              # will be maped to 0
    "src_bytes": 181,
    "dst_bytes": 5450,
    "land": 0,
    "wrong_fragment": 0,
    "urgent": 0,
    "hot": 0,
    "num_failed_logins": 0,
    "logged_in": 1,
    "num_compromised": 0,
    "root_shell": 0,
    "su_attempted": 0,
    "num_file_creations": 0,
    "num_shells": 0,
    "num_access_files": 0,
    "is_guest_login": 0,
    "count": 8,
    "srv_count": 8,
    "serror_rate": 0.0,
    "rerror_rate": 0.0,
    "same_srv_rate": 1.0,
    "diff_srv_rate": 0.0,
    "srv_diff_host_rate": 0.0,
    "dst_host_count": 9,
    "dst_host_srv_count": 9,
    "dst_host_same_srv_rate": 1.0,
    "dst_host_diff_srv_rate": 0.0,
    "dst_host_same_src_port_rate": 0.11,
    "dst_host_srv_diff_host_rate": 0.0,
    "time": 1617656527 
}

def test_prediction():
    try:
        response = requests.post(url_docker, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print("Prediction result:")
            print(json.dumps(result, indent=4))
        else:
            print(f"Error: Received status code {response.status_code}")
            print(response.json())
            
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    test_prediction()
