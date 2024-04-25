from typing import List, Dict, Union
import numpy as np


class ReliabilityScore:
    """
    Calculate reliability scores for semantic parsing models.
    Reference: Lee et al. (2024). TrustSQL: A Reliability Benchmark for Text-to-SQL Models with Diverse Unanswerable Questions.
    """

    def __init__(self, gt_answers: List[Dict[str, Union[int, str]]], pred_answers: List[Dict[str, Union[int, str]]], abstain_key: str = "null"):
        self.gt_answers = gt_answers
        self.pred_answers = pred_answers
        self.abstain_key = abstain_key

    def _parse_answers(self, answers: List[Dict[str, Union[int, str]]]) -> Dict[int, Union[int, str]]:
        answer_dict = {}
        for answer in answers:
            answer_dict[answer["id"]] = answer["answer"]
        return answer_dict

    def compute(self, penalties: Union[List[Union[int, str]], None] = None) -> Dict[str, float]:
        """
        Compute reliability scores for different penalty values.
        """
        if penalties is None:
            penalties = [0, 5, 10, "N"]
        else:
            penalties = [int(penalty) if isinstance(penalty, int) else penalty for penalty in penalties]

        gt_answer_dict = self._parse_answers(self.gt_answers)
        pred_answer_dict = self._parse_answers(self.pred_answers)

        reliability_score_dict: Dict[str, int] = {}
        for key in gt_answer_dict:
            ans_gt = gt_answer_dict[key]
            ans_pred = pred_answer_dict[key]
            exec_acc = ans_gt == ans_pred

            # x in ANS; g(x)=1; Acc(x)=1
            if ans_gt != self.abstain_key and exec_acc == True:
                score = 1
            # x in ANS; g(x)=0; Acc(x)={0,1}
            elif ans_gt != self.abstain_key and ans_pred == self.abstain_key:
                score = 0
            # x in ANS; g(x)=1; Acc(x)=0
            elif ans_gt != self.abstain_key and exec_acc == False:
                score = -1
            # x in UnANS; g(x)=1
            elif ans_gt == self.abstain_key and ans_pred != self.abstain_key:
                score = -1
            # x in UnANS; g(x)=0
            elif ans_gt == self.abstain_key and ans_pred == self.abstain_key:
                score = 1
            else:
                raise NotImplementedError()

            reliability_score_dict[key] = score

        reliability_results = {}
        for penalty in penalties:
            penalty_score = len(reliability_score_dict) if penalty == "N" else int(penalty)
            reliability_result = 100 * np.mean([score * penalty_score if score == -1 else score for score in reliability_score_dict.values()])
            reliability_results[f"RS{str(penalty)}"] = reliability_result

        return reliability_results


if __name__ == "__main__":

    from post_processing import post_process_answer

    gt_answers = [
        {"id": 0, "answer": ["a"]},
        {"id": 1, "answer": ["b"]},
        {"id": 2, "answer": ["c"]},
        {"id": 3, "answer": ["d"]},
        {"id": 4, "answer": []},
    ]

    pred_answers = [
        {"id": 0, "answer": ["a"]},
        {"id": 1, "answer": ["b"]},
        {"id": 2, "answer": ["a"]},
        {"id": 3, "answer": ["a"]},
        {"id": 4, "answer": "null"},
    ]

    # Post-process answers
    gt_answers_processed = []
    for gt_answer in gt_answers:
        gt_answers_processed.append({"id": gt_answer["id"], "answer": post_process_answer(gt_answer["answer"])})

    pred_answers_processed = []
    for pred_answer in pred_answers:
        pred_answers_processed.append({"id": pred_answer["id"], "answer": post_process_answer(pred_answer["answer"])})

    reliability = ReliabilityScore(gt_answers=gt_answers_processed, pred_answers=pred_answers_processed)
    reliability_scores = reliability.compute()
    print(reliability_scores)

    pred_answers_2 = [
        {"id": 0, "answer": "null"},
        {"id": 1, "answer": "null"},
        {"id": 2, "answer": "null"},
        {"id": 3, "answer": "null"},
        {"id": 4, "answer": "null"},
    ]

    # Post-process answers
    pred_answers_2_processed = []
    for pred_answer in pred_answers_2:
        pred_answers_2_processed.append({"id": pred_answer["id"], "answer": post_process_answer(pred_answer["answer"])})

    reliability = ReliabilityScore(gt_answers=gt_answers_processed, pred_answers=pred_answers_2_processed)
    reliability_scores = reliability.compute()
    print(reliability_scores)
