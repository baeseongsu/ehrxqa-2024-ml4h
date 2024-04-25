import json

# custom package
from reliability_score import ReliabilityScore
from post_processing import post_process_answer


def evaluate(gt_answers, pred_answers):

    assert len(gt_answers) == len(pred_answers), "Number of answers in GT and prediction are not equal"

    assert isinstance(gt_answers, list), "GT answers should be a list"
    assert isinstance(pred_answers, list), "Prediction answers should be a list"

    # compute reliability scores
    reliability = ReliabilityScore(
        gt_answers=gt_answers,
        pred_answers=pred_answers,
        abstain_key="null",
    )
    reliability_scores = reliability.compute(penalties=["0", "5", "10", "N"])
    print(reliability_scores)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--gt_answers_path", "-gt_path", type=str, required=True, help="Path to the ground truth answers")
    parser.add_argument("--pred_answers_path", "-pred_path", type=str, required=True, help="Path to the predicted answers")
    args = parser.parse_args()

    gt_answers = json.load(open(args.gt_answers_path))
    pred_answers = json.load(open(args.pred_answers_path))
    evaluate(
        gt_answers_path=args.gt_answers_path,
        pred_answers_path=args.pred_answers_path,
    )
