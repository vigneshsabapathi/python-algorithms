def calculate_span(price: list[int]) -> list[int]:
    """
    Calculate the span values for a given list of stock prices.
    The span of a stock price on a given day is the maximum number of
    consecutive days just before the given day for which the price is
    less than or equal to the price on that day.

    >>> calculate_span([10, 4, 5, 90, 120, 80])
    [1, 1, 2, 4, 5, 1]
    >>> calculate_span([100, 50, 60, 70, 80, 90])
    [1, 1, 2, 3, 4, 5]
    >>> calculate_span([5, 4, 3, 2, 1])
    [1, 1, 1, 1, 1]
    >>> calculate_span([1, 2, 3, 4, 5])
    [1, 2, 3, 4, 5]
    >>> calculate_span([10, 20, 30, 40, 50])
    [1, 2, 3, 4, 5]
    >>> calculate_span([100, 80, 60, 70, 60, 75, 85])
    [1, 1, 1, 2, 1, 4, 6]
    """
    n = len(price)
    s = [0] * n
    st = []
    st.append(0)
    s[0] = 1

    for i in range(1, n):
        while len(st) > 0 and price[st[-1]] <= price[i]:
            st.pop()

        s[i] = i + 1 if len(st) <= 0 else (i - st[-1])
        st.append(i)

    return s


def print_array(arr, n):
    for i in range(n):
        print(arr[i], end=" ")


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    price = [10, 4, 5, 90, 120, 80]
    S = calculate_span(price)
    print_array(S, len(price))
