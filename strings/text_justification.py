def text_justification(word: str, max_width: int) -> list:
    """
    Will format the string such that each line has exactly
    (max_width) characters and is fully (left and right) justified,
    and return the list of justified text.

    example 1:
    string = "This is an example of text justification."
    max_width = 16

    output = ['This    is    an',
              'example  of text',
              'justification.  ']

    >>> text_justification("This is an example of text justification.", 16)
    ['This    is    an', 'example  of text', 'justification.  ']

    example 2:
    string = "Two roads diverged in a yellow wood"
    max_width = 16
    output = ['Two        roads',
              'diverged   in  a',
              'yellow wood     ']

    >>> text_justification("Two roads diverged in a yellow wood", 16)
    ['Two        roads', 'diverged   in  a', 'yellow wood     ']

    Time complexity: O(m*n)
    Space complexity: O(m*n)
    """

    # Split the input string into individual words
    words = word.split()

    def justify(line: list, width: int, max_width: int) -> str:
        # Total spaces to distribute across the gaps between words
        overall_spaces_count = max_width - width
        words_count = len(line)

        if len(line) == 1:
            # Single word: pad with trailing spaces to reach max_width
            return line[0] + " " * overall_spaces_count
        else:
            spaces_to_insert_between_words = words_count - 1

            # Base number of spaces for each gap (floor division)
            num_spaces_between_words_list = spaces_to_insert_between_words * [
                overall_spaces_count // spaces_to_insert_between_words
            ]

            # Remainder spaces distributed left-to-right (round robin)
            spaces_count_in_locations = (
                overall_spaces_count % spaces_to_insert_between_words
            )
            for i in range(spaces_count_in_locations):
                num_spaces_between_words_list[i] += 1

            # Build the justified line: word, spaces, word, spaces, ..., last word
            aligned_words_list = []
            for i in range(spaces_to_insert_between_words):
                aligned_words_list.append(line[i])
                aligned_words_list.append(num_spaces_between_words_list[i] * " ")
            aligned_words_list.append(line[-1])

            return "".join(aligned_words_list)

    answer = []
    line: list[str] = []
    width = 0

    for inner_word in words:
        # Check if adding this word (plus one space per existing word) fits on the line
        if width + len(inner_word) + len(line) <= max_width:
            line.append(inner_word)
            width += len(inner_word)
        else:
            # Current line is full — justify it and start a new one
            answer.append(justify(line, width, max_width))
            line, width = [inner_word], len(inner_word)

    # Last line: left-aligned (words joined by single spaces, trailing spaces to fill)
    remaining_spaces = max_width - width - len(line)
    answer.append(" ".join(line) + (remaining_spaces + 1) * " ")

    return answer


if __name__ == "__main__":
    from doctest import testmod

    testmod()
