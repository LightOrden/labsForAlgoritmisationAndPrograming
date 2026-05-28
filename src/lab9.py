def compute_prefix_function(pattern: str) -> list[dict]:
    m = len(pattern)
    delta = [{} for _ in range(m + 1)]
    for q in range(m + 1):
        for ch in set(pattern):
            k = min(m, q + 1)
            s = pattern[:q] + ch
            while k > 0 and not s.endswith(pattern[:k]):
                k -= 1
            delta[q][ch] = k
    return delta


def fa_find_all(text: str, pattern: str) -> list[int]:
    """Повертає список стартових індексів усіх входжень pattern у text."""
    if not pattern or not text:
        return []
    m = len(pattern)
    transition = compute_prefix_function(pattern)
    q = 0
    result = []
    for pos, symbol in enumerate(text):
        q = transition[q].get(symbol, 0)
        if q == m:
            result.append(pos - m + 1)
    return result


if __name__ == "__main__":
    sample_text    = "ABCABCABCABC"
    sample_pattern = "ABCAB"
    found = fa_find_all(sample_text, sample_pattern)
    print(f"Шаблон '{sample_pattern}' знайдено на позиціях: {found}")