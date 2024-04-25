import os
import json
from evaluate import evaluate


def predict(data):
    predictions = []
    for entry in data:
        predictions.append({"id": entry["id"], "answer": "null"})
    return predictions


def _debug():
    with open("../dataset/mimic_iv_cxr/train/train_data.json") as f:
        train_data = json.load(f)
    with open("../dataset/mimic_iv_cxr/train/train_answer.json") as f:
        train_answer = json.load(f)

    evaluate(
        gt_answers=train_answer,
        pred_answers=predict(train_data),
    )


def main():
    _debug()

    os.makedirs("results", exist_ok=True)

    # read data and prediciton and make submission zip file
    with open("../dataset/mimic_iv_cxr/valid/valid_data.json") as f:
        valid_data = json.load(f)

    valid_answer = predict(valid_data)
    # build the zip file
    with open("results/baseline_submission.json", "w") as f:
        json.dump(valid_answer, f)

    os.system("cd results && zip baseline_submission.zip baseline_submission.json")


if __name__ == "__main__":
    main()
