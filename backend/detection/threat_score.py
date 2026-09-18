def calculate_threat_score(
    packet_size,
    protocol,
    destination_port
):

    score = 0

    if packet_size > 1500:
        score += 40

    if protocol == "ICMP":
        score += 30

    if destination_port in [22, 23, 445, 3389]:
        score += 30

    score = min(score, 100)

    if score >= 70:
        risk = "HIGH"

    elif score >= 40:
        risk = "MEDIUM"

    else:
        risk = "LOW"

    return score, risk