# Strings

A collection of 51 string algorithms implemented in Python — each with doctests, live-tested output, and where applicable an optimized variant with benchmarks.

---

## Algorithms

| Algorithm | File | Optimized | Category |
|-----------|------|-----------|----------|
| Aho-Corasick | [aho_corasick.py](aho_corasick.py) | [optimized](aho_corasick_optimized.py) | Multi-pattern search |
| Alternative String Arrange | [alternative_string_arrange.py](alternative_string_arrange.py) | [optimized](alternative_string_arrange_optimized.py) | String manipulation |
| Anagrams | [anagrams.py](anagrams.py) | [optimized](anagrams_optimized.py) | Hashing / grouping |
| Autocomplete Using Trie | [autocomplete_using_trie.py](autocomplete_using_trie.py) | [optimized](autocomplete_using_trie_optimized.py) | Trie / prefix search |
| Barcode Validator | [barcode_validator.py](barcode_validator.py) | [optimized](barcode_validator_optimized.py) | Validation / check digit |
| Bitap String Match | [bitap_string_match.py](bitap_string_match.py) | [optimized](bitap_string_match_optimized.py) | Approximate matching |
| Boyer-Moore Search | [boyer_moore_search.py](boyer_moore_search.py) | [optimized](boyer_moore_search_optimized.py) | Pattern matching |
| Camel Case to Snake Case | [camel_case_to_snake_case.py](camel_case_to_snake_case.py) | [optimized](camel_case_to_snake_case_optimized.py) | Case conversion |
| Can String Be Rearranged as Palindrome | [can_string_be_rearranged_as_palindrome.py](can_string_be_rearranged_as_palindrome.py) | [optimized](can_string_be_rearranged_as_palindrome_optimized.py) | Palindrome / frequency |
| Capitalize | [capitalize.py](capitalize.py) | [optimized](capitalize_optimized.py) | String manipulation |
| Check Anagrams | [check_anagrams.py](check_anagrams.py) | [optimized](check_anagrams_optimized.py) | Hashing / frequency |
| Count Vowels | [count_vowels.py](count_vowels.py) | [optimized](count_vowels_optimized.py) | String analysis |
| Credit Card Validator | [credit_card_validator.py](credit_card_validator.py) | [optimized](credit_card_validator_optimized.py) | Validation / Luhn |
| Damerau-Levenshtein Distance | [damerau_levenshtein_distance.py](damerau_levenshtein_distance.py) | [optimized](damerau_levenshtein_optimized.py) | Edit distance / DP |
| Detecting English Programmatically | [detecting_english_programmatically.py](detecting_english_programmatically.py) | [optimized](detecting_english_optimized.py) | Language detection |
| DNA | [dna.py](dna.py) | [optimized](dna_optimized.py) | Encoding / biology |
| Frequency Finder | [frequency_finder.py](frequency_finder.py) | [optimized](frequency_finder_optimized.py) | String analysis |
| Hamming Distance | [hamming_distance.py](hamming_distance.py) | [optimized](hamming_distance_optimized.py) | Edit distance |
| Is Contains Unique Chars | [is_contains_unique_chars.py](is_contains_unique_chars.py) | [optimized](is_contains_unique_chars_optimized.py) | Validation |
| Is Indian Phone Number | [is_indian_phone_number.py](is_indian_phone_number.py) | — | Validation / regex |
| Is Isogram | [is_isogram.py](is_isogram.py) | [optimized](is_isogram_optimized.py) | Validation |
| Is Pangram | [is_pangram.py](is_pangram.py) | — | Validation |
| Is Spain National ID | [is_spain_national_id.py](is_spain_national_id.py) | — | Validation / check digit |
| Is Valid Email Address | [is_valid_email_address.py](is_valid_email_address.py) | — | Validation / regex |
| Jaro-Winkler Distance | [jaro_winkler.py](jaro_winkler.py) | — | Similarity / fuzzy match |
| Join | [join.py](join.py) | — | String manipulation |
| Knuth-Morris-Pratt (KMP) | [knuth_morris_pratt.py](knuth_morris_pratt.py) | — | Pattern matching |
| Levenshtein Distance | [levenshtein_distance.py](levenshtein_distance.py) | — | Edit distance / DP |
| Lower | [lower.py](lower.py) | — | Case conversion |
| Manacher's Algorithm | [manacher.py](manacher.py) | — | Palindrome / linear |
| Min Cost String Conversion | [min_cost_string_conversion.py](min_cost_string_conversion.py) | — | Edit distance / DP |
| N-gram | [ngram.py](ngram.py) | — | NLP / tokenization |
| Naive String Search | [naive_string_search.py](naive_string_search.py) | — | Pattern matching |
| Palindrome | [palindrome.py](palindrome.py) | — | Palindrome |
| Pig Latin | [pig_latin.py](pig_latin.py) | — | String transformation |
| Prefix Function (KMP) | [prefix_function.py](prefix_function.py) | — | Pattern matching |
| Rabin-Karp | [rabin_karp.py](rabin_karp.py) | — | Pattern matching / hash |
| Remove Duplicate Words | [remove_duplicate.py](remove_duplicate.py) | — | String manipulation |
| Reverse Letters | [reverse_letters.py](reverse_letters.py) | — | String manipulation |
| Reverse Words | [reverse_words.py](reverse_words.py) | — | String manipulation |
| Snake Case to Camel/Pascal Case | [snake_case_to_camel_pascal_case.py](snake_case_to_camel_pascal_case.py) | — | Case conversion |
| Split | [split.py](split.py) | — | String manipulation |
| String Switch Case | [string_switch_case.py](string_switch_case.py) | — | Case conversion |
| Strip | [strip.py](strip.py) | — | String manipulation |
| Text Justification | [text_justification.py](text_justification.py) | — | Formatting |
| Title Case | [title.py](title.py) | — | Case conversion |
| Top K Frequent Words | [top_k_frequent_words.py](top_k_frequent_words.py) | — | Frequency / heap |
| Upper | [upper.py](upper.py) | — | Case conversion |
| Wave String | [wave_string.py](wave_string.py) | — | String rearrangement |
| Wildcard Pattern Matching | [wildcard_pattern_matching.py](wildcard_pattern_matching.py) | — | Pattern matching / DP |
| Word Occurrence | [word_occurrence.py](word_occurrence.py) | — | Frequency / counting |
| Word Pattern | [word_pattern.py](word_pattern.py) | — | Pattern matching |

---

## Categories

### Pattern Matching
Algorithms that find one or more patterns within a text string.

| Algorithm | Complexity | Key Technique |
|-----------|-----------|---------------|
| Aho-Corasick | O(n + matches) search | Finite automaton + fail links |
| Bitap (Shift-Or) | O(n × m/w) | Bitmask operations |
| Boyer-Moore | O(n/m) best case | Bad-char + good-suffix skip |
| Knuth-Morris-Pratt | O(n + m) | Failure function / prefix array |
| Naive String Search | O(n × m) | Brute force sliding window |
| Prefix Function | O(n + m) | KMP failure function |
| Rabin-Karp | O(n + m) avg | Rolling polynomial hash |
| Wildcard Pattern Matching | O(n × m) | DP with `*` and `?` wildcards |

### Edit Distance / Dynamic Programming
Algorithms that measure or minimise the cost to transform one string into another.

| Algorithm | Complexity | Key Technique |
|-----------|-----------|---------------|
| Damerau-Levenshtein | O(n × m) | DP + transposition |
| Hamming Distance | O(n) | Positional XOR / zip |
| Levenshtein Distance | O(n × m) | Classic edit distance DP |
| Min Cost String Conversion | O(n × m) | DP with custom costs |

### Similarity / Fuzzy Matching
| Algorithm | Use Case |
|-----------|---------|
| Jaro-Winkler Distance | Name matching, record linkage |

### Trie / Prefix Structures
| Algorithm | Key Feature |
|-----------|-------------|
| Autocomplete Using Trie | Prefix → all completions |
| Aho-Corasick | Multi-keyword search via shared trie |

### Validation
| Algorithm | Validates |
|-----------|-----------|
| Barcode Validator | EAN-13 check digit |
| Credit Card Validator | Luhn algorithm |
| Is Contains Unique Chars | All chars distinct |
| Is Indian Phone Number | Indian mobile format |
| Is Isogram | No repeated letters |
| Is Pangram | All 26 letters present |
| Is Spain National ID | Spanish DNI check digit |
| Is Valid Email Address | RFC-style email format |

### Hashing / Grouping
| Algorithm | Key Idea |
|-----------|---------|
| Anagrams | Group words by sorted-char signature |
| Check Anagrams | Compare two words for anagram |
| Frequency Finder | Character frequency map |
| Top K Frequent Words | Heap-based top-k |
| Word Occurrence | Word frequency count |

### Palindrome
| Algorithm | Approach |
|-----------|---------|
| Can String Be Rearranged as Palindrome | Odd-frequency count |
| Manacher's Algorithm | O(n) longest palindromic substring |
| Palindrome | O(n) two-pointer check |

### Case Conversion & Formatting
| Algorithm | Converts |
|-----------|---------|
| Camel Case to Snake Case | `camelCase` → `snake_case` |
| Capitalize | First letter uppercase |
| Lower / Upper | Full case conversion |
| Snake Case to Camel/Pascal | `snake_case` → `camelCase` / `PascalCase` |
| String Switch Case | Toggle each character's case |
| Text Justification | Align words to fixed width |
| Title Case | Capitalise each word |

### String Manipulation
| Algorithm | What It Does |
|-----------|-------------|
| Alternative String Arrange | Interleave two strings |
| Join | Custom string join |
| N-gram | Extract character/word n-grams |
| Pig Latin | Translate to Pig Latin |
| Remove Duplicate Words | Deduplicate words in a string |
| Reverse Letters | Reverse each word's letters |
| Reverse Words | Reverse word order |
| Split | Custom string split |
| Strip | Remove leading/trailing chars |
| Wave String | Arrange in wave pattern |
| Word Pattern | Match string to abstract pattern |

### Encoding / Other
| Algorithm | Domain |
|-----------|--------|
| Detecting English Programmatically | Cipher / cryptanalysis |
| DNA | Nucleotide encoding |

---

## Benchmark Highlights

Optimized variants that showed the largest speedups:

| Algorithm | Speedup | Technique |
|-----------|---------|-----------|
| Anagrams | ~9.9× | `tuple(sorted(word))` vs `Counter` + format string |
| Aho-Corasick search | 4.45× | Precomputed goto dict vs linear child scan + while-loop |
| Autocomplete query | 1.6× | Iterative DFS + `is_end` bool vs recursive sentinel walk |
| Alternative String Arrange | 1.61× | `zip_longest` + `chain` vs manual index loop |

---

## Running the Tests

```bash
# Run all doctests for a single file
python -m doctest strings/aho_corasick.py -v

# Run doctests for every file in the folder
for f in strings/*.py; do python -m doctest "$f"; done

# Run a specific algorithm
python strings/aho_corasick.py

# Run benchmark for an optimized variant
python strings/aho_corasick_optimized.py
```

---

## Dictionary File

Several algorithms (`anagrams.py`, `detecting_english_programmatically.py`) load `strings/words.txt` — a 234,371-word English dictionary included in this repo.
