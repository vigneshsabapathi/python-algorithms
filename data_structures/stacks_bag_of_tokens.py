"""
Bag of Tokens - LeetCode problem 948.
https://leetcode.com/problems/bag-of-tokens/

You have an initial power of P, an initial score of 0, and a bag of tokens
where tokens[i] is the value of the ith token (0-indexed).

You want to maximize your total score by potentially playing each token in one
of two ways:
- If your current power >= tokens[i], you may play token i face up, losing
  tokens[i] power and gaining 1 score.
- If your current score >= 1, you may play token i face down, gaining
  tokens[i] power and losing 1 score.

Return the largest possible score you can achieve.
"""


def bag_of_tokens_score(tokens: list[int], power: int) -> int:
    """
    Find the maximum score achievable from bag of tokens.

    Uses a two-pointer greedy approach:
    - Sort tokens
    - Use smallest token to buy score when possible
    - Use largest token to regain power when needed

    >>> bag_of_tokens_score([100], 50)
    0
    >>> bag_of_tokens_score([100, 200], 150)
    1
    >>> bag_of_tokens_score([100, 200, 300, 400], 200)
    2
    >>> bag_of_tokens_score([], 100)
    0
    >>> bag_of_tokens_score([71, 55, 82], 54)
    0
    >>> bag_of_tokens_score([100], 100)
    1
    """
    tokens.sort()
    left, right = 0, len(tokens) - 1
    score = 0
    max_score = 0

    while left <= right:
        if power >= tokens[left]:
            # Play face up: spend power, gain score
            power -= tokens[left]
            score += 1
            left += 1
            max_score = max(max_score, score)
        elif score > 0 and left < right:
            # Play face down: gain power, lose score
            power += tokens[right]
            score -= 1
            right -= 1
        else:
            break

    return max_score


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(bag_of_tokens_score([100, 200, 300, 400], 200))
