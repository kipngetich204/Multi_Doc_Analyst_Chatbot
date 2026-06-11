class EvaluationSuite:
    def precision_at_k(self, retrieved, relevant, k):
        retrieved_k = retrieved[:k]
        relevant_found = len(set(retrieved_k) & set(relevant))

        return relevant_found / k

    def recall_at_k(self, retrieved, relevant, k):
        retrieved_k = retrieved[:k]
        relevant_found = len(set(retrieved_k) & set(relevant))

        return relevant_found / len(relevant)

    def mrr(self, retrieved, relevant):
        for idx, item in enumerate(retrieved, start=1):
            if item in relevant:
                return 1 / idx

        return 0