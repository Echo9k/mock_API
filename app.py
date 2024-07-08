import os
import json
import ray
from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize Ray with appropriate resources
ray.init(
    _memory=2 * 1024 * 1024 * 1024,  # 2GB memory
    object_store_memory=512 * 1024 * 1024  # 512MB object store memory
)

@ray.remote
def process_request(data, is_accepted=True, seed=42):
    response = {
        "status": "Done",
        "document_id": "string",
        "result": {
            "PackageStatus": "string",
            "PackageStatusScore": 100,
            "Fraud": False,
            "center_alignment": True,
            "Blurriness": False,
            "BatchId": "16JUN24GD4A0909:53JB",
            "EAN": "7501011127012",
            "Remark": "accept",
            "Comment": "ok",
            "fresh_by_date": "16JUN24",
            "plant": "GD",
            "line": "09",
            "day_of_week": "4",
            "shift": "A",
            "time": "09:53",
            "operator": "JB",
            "Coupon": "None",
            "od_result_box": [
                [1528, 554, 1728, 699],
                [1806, 1643, 3735, 1807],
                [2219, 1061, 2510, 1479],
                [126, 64, 3826, 1730]
            ],
            "od_result_label": [
                "BatchId_92",
                "PacketEnd_87",
                "Barcode_94",
                "Package_89"
            ],
            "BatchidBlurValue": 36.11687972933501,
            "BarcodeBlurValue": 73.33854939656592
        }
    }

    if is_accepted is not None:
        response['result']['Remark'] = "accept" if is_accepted else "reject"
    if seed is not None:
        response['seed'] = seed

    return response

@app.route('/image_recognition/api1', methods=['POST'])
def api1():
    data = request.json
    is_accepted = data.get('is_accepted')
    seed = data.get('seed')

    future = process_request.remote(data, is_accepted, seed)
    response = ray.get(future)

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
