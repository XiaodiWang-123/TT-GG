# ddti_sbs_helper.py

def ask_score(name):
    print(f"\n{name}")
    print("选项：")
    print("  2  = TT dramatically better than GG")
    print("  1  = TT slightly better than GG")
    print("  0  = Equal / no clear difference")
    print(" -1  = TT slightly worse than GG")
    print(" -2  = TT dramatically worse than GG")

    while True:
        s = input(f"请输入 {name} 分数 (-2/-1/0/1/2): ").strip()
        if s in ["-2", "-1", "0", "1", "2"]:
            return int(s)
        print("只能输入 -2, -1, 0, 1, 2")


def ask_yes_no(q):
    while True:
        a = input(q + " (y/n): ").strip().lower()
        if a in ["y", "yes"]:
            return True
        if a in ["n", "no"]:
            return False
        print("请输入 y 或 n")


def side_word(score):
    if score < 0:
        return "TT is worse than GG"
    if score > 0:
        return "TT is better than GG"
    return "TT and GG are equal"


def strength_word(score):
    if abs(score) == 2:
        return "dramatically"
    if abs(score) == 1:
        return "slightly"
    return ""


def reason_amount(score, details):
    if score == 0:
        return ""
    side = side_word(score)
    return f"{side} in amount of information because {details}. Overall, TT provides {strength_word(score)} {'less' if score < 0 else 'more'} information than GG."


def reason_quality(score, details):
    if score == 0:
        return ""
    side = side_word(score)
    return f"{side} in quality of information because {details}. The information/media on TT is {strength_word(score)} {'lower' if score < 0 else 'higher'} quality than GG."


def reason_relevance(score, details):
    if score == 0:
        return ""
    side = side_word(score)
    return f"{side} in relevance of information because {details}. This makes TT {strength_word(score)} {'less' if score < 0 else 'more'} relevant than GG."


def reason_overall(score, amount, quality, relevance):
    if score == 0:
        return ""
    if score < 0:
        return (
            f"Based on the screen, TT is {strength_word(score)} worse than GG overall. "
            f"The main gaps come from amount ({amount}), quality ({quality}), and relevance ({relevance}). "
            f"GG gives users clearer and more useful information for making a decision."
        )
    return (
        f"Based on the screen, TT is {strength_word(score)} better than GG overall. "
        f"TT provides stronger information across amount ({amount}), quality ({quality}), and relevance ({relevance}), "
        f"making the page more useful for users."
    )


def collect_dimension(prefix, col_amount, col_quality, col_relevance, col_overall, col_reason):
    print(f"\n========== {prefix} ==========")

    amount = ask_score(f"{prefix} - Amount of information")
    amount_detail = ""
    if amount != 0:
        amount_detail = input("为什么 amount 不是 0？例如：GG has menu/wait time/website/images, TT lacks them: ")

    quality = ask_score(f"{prefix} - Quality of information")
    quality_detail = ""
    if quality != 0:
        quality_detail = input("为什么 quality 不是 0？例如：TT lacks star rating / bad cover image / low trust reviews: ")

    relevance = ask_score(f"{prefix} - Relevance of information")
    relevance_detail = ""
    if relevance != 0:
        relevance_detail = input("为什么 relevance 不是 0？例如：TT cover image is logo / posts irrelevant / info not useful: ")

    overall = ask_score(f"{prefix} - Overall screen efficiency GSB")

    reasons = []
    if amount != 0:
        reasons.append(reason_amount(amount, amount_detail))
    if quality != 0:
        reasons.append(reason_quality(quality, quality_detail))
    if relevance != 0:
        reasons.append(reason_relevance(relevance, relevance_detail))
    if overall != 0:
        reasons.append(reason_overall(overall, amount, quality, relevance))

    return {
        col_amount: amount,
        col_quality: quality,
        col_relevance: relevance,
        col_overall: overall,
        col_reason: " ".join(reasons)
    }


def collect_single_score(title, score_col, issue_col, remarks_col):
    print(f"\n========== {title} ==========")
    score = ask_score(title)
    issue = ""
    remarks = ""

    if score != 0:
        issue = input("Issue classification 写什么？例如 Missing trust signals / Insufficient reviews quantity / Bad quality posts: ")
        remarks = input("Remarks / Reasons 写什么？具体说明 TT 和 GG 差异: ")

    return {
        score_col: score,
        issue_col: issue,
        remarks_col: remarks
    }


def main():
    print("SBS Helper - TT vs GG")
    poi = input("POI name: ")
    category = input("Category，例如 Dining / Hotel / Travel / Beauty: ")

    result = {}
    result["POI"] = poi
    result["Category"] = category

    # N - T: First screen
    result.update(collect_dimension(
        "First screen",
        "N Amount of information",
        "O Quality of information",
        "P Relevance of information",
        "R First screen efficiency GSB",
        "T Reason"
    ))

    # U - AA: Overall screen
    result.update(collect_dimension(
        "Overall screen",
        "U Amount of information",
        "V Quality of information",
        "W Relevance of information",
        "Y Overall screen efficiency GSB",
        "AA Remarks"
    ))

    # AF - AH Star rating
    result.update(collect_single_score(
        "Star rating",
        "AF Star rating",
        "AG Issue classification",
        "AH Reasons"
    ))

    # AI - AN Reviews
    result.update(collect_single_score(
        "Reviews",
        "AI Equal / Good / Bad",
        "AM Issue classification",
        "AN Remarks"
    ))

    tt_reviews = input("\nAK TT number of Reviews: ")
    gg_reviews = input("AL GG number of Reviews: ")
    result["AK TT number of Reviews"] = tt_reviews
    result["AL GG number of Reviews"] = gg_reviews

    # AO - AR Static images
    result.update(collect_single_score(
        "Static images",
        "AO Equal / Good / Bad",
        "AQ Issue classification",
        "AR Remarks"
    ))

    # AS - AV Posts
    result.update(collect_single_score(
        "Posts",
        "AS Equal / Good / Bad",
        "AU Issue classification",
        "AV Remarks"
    ))

    # AW - AZ Highlights
    result.update(collect_single_score(
        "Highlights",
        "AW Equal / Good / Bad",
        "AY Issue classification",
        "AZ Remarks"
    ))

    print("\n\n================ FINAL RESULT ================")
    for col, value in result.items():
        if value != "":
            print(f"{col}: {value}")

    print("\n复制上面的内容到对应 Excel columns。")


if __name__ == "__main__":
    main()
