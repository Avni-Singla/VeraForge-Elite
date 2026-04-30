def score_trigger(trigger: dict, merchant: dict):
    scores = {}

    sales_dip = trigger.get("sales_dip", 0)
    search_spike = trigger.get("search_spike", 0)
    inactive_customers = trigger.get("inactive_customers", 0)
    rating_drop = trigger.get("rating_drop", 0)
    festival = trigger.get("festival", False)

    scores["search_spike"] = search_spike * 3
    scores["sales_dip"] = sales_dip * 2
    scores["inactive_customers"] = inactive_customers * 2.5
    scores["rating_drop"] = rating_drop * 2

    if festival:
        scores["festival"] = 15

    best_trigger = max(scores, key=scores.get)
    return best_trigger, scores