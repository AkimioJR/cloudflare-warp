def compare_versions(v1: str, v2: str) -> int:
    """
    compare_versions compares two version strings (e.g., "1.2.3" and "1.2.4").
    It returns:
        - 1 if v1 > v2
        - -1 if v1 < v2
        - 0 if v1 == v2
    """
    parts1 = list(map(int, v1.split(".")))
    parts2 = list(map(int, v2.split(".")))

    # 补齐长度
    max_len = max(len(parts1), len(parts2))
    parts1 += [0] * (max_len - len(parts1))
    parts2 += [0] * (max_len - len(parts2))

    for p1, p2 in zip(parts1, parts2):
        if p1 > p2:
            return 1
        elif p1 < p2:
            return -1
    return 0
