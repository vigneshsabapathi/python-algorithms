# Python Algorithms

> A complete reference implementation of **867+ algorithms** across **39 domains** — each with clean doctests, 3+ optimized variants, and benchmarked comparisons. Built for interview prep and deep understanding.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Algorithms](https://img.shields.io/badge/Algorithms-867%2B-success?style=flat-square)
![Categories](https://img.shields.io/badge/Categories-39-blueviolet?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)
![Tests](https://img.shields.io/badge/Tests-doctests%20verified-brightgreen?style=flat-square)

---

## Quick Start

```bash
git clone https://github.com/vigneshsabapathi/python-algorithms
cd python-algorithms
python -m venv venv && venv/Scripts/activate    # Windows
# source venv/bin/activate                      # macOS/Linux
pip install -r requirements.txt

# Run any algorithm
python -m doctest sorts/merge_sort.py -v
python -c "from sorts.merge_sort import merge_sort; print(merge_sort([3,1,4,1,5]))"
```

---

## Repository Structure

Every algorithm follows the same pattern:

```
category/
├── algorithm_name.py           # Clean implementation + doctests
└── algorithm_name_optimized.py # 3+ variants with benchmark()
```

| File | Purpose |
|------|---------|
| `algorithm.py` | Single canonical implementation, fully tested with `doctest` |
| `algorithm_optimized.py` | 2–4 alternative approaches + `benchmark()` with `timeit` |

---

## Category Index

| # | Category | Algorithms | Highlights |
|---|----------|-----------|------------|
| 1 | [Audio Filters](#audio-filters) | 3 | Butterworth, IIR |
| 2 | [Backtracking](#backtracking) | 20 | N-Queens, Knight Tour, Sudoku |
| 3 | [Bit Manipulation](#bit-manipulation) | 26 | Gray Code, Brian Kernighan, XOR tricks |
| 4 | [Blockchain](#blockchain) | 1 | Diophantine Equation |
| 5 | [Boolean Algebra](#boolean-algebra) | 12 | All gates, Karnaugh map, Quine-McCluskey |
| 6 | [Cellular Automata](#cellular-automata) | 6 | Conway's Game of Life, Langton's Ant |
| 7 | [Ciphers](#ciphers) | 47 | RSA, Enigma, Vigenère, AES-style |
| 8 | [Computer Vision](#computer-vision) | 9 | Harris Corner, CNN, Horn-Schunck |
| 9 | [Conversions](#conversions) | 31 | Base, Unit, RGB, Roman numerals |
| 10 | [Data Compression](#data-compression) | 8 | Huffman, LZ77, Burrows-Wheeler |
| 11 | [Data Structures](#data-structures) | 88 | Trees, Heaps, Tries, Skip List |
| 12 | [Digital Image Processing](#digital-image-processing) | 20 | Edge detection, Filters, Morphology |
| 13 | [Divide & Conquer](#divide--conquer) | 12 | Strassen, Closest Pair, Karatsuba |
| 14 | [Dynamic Programming](#dynamic-programming) | 50 | LCS, Knapsack, Edit Distance, Viterbi |
| 15 | [Electronics](#electronics) | 19 | Ohm's Law, 555 Timer, Wheatstone Bridge |
| 16 | [Financial](#financial) | 8 | EMI, Moving Average, Present Value |
| 17 | [Fractals](#fractals) | 5 | Mandelbrot, Koch, Sierpiński |
| 18 | [Fuzzy Logic](#fuzzy-logic) | 1 | Fuzzy Operations |
| 19 | [Genetic Algorithm](#genetic-algorithm) | 1 | Basic String Evolution |
| 20 | [Geodesy](#geodesy) | 2 | Haversine, Lambert's Ellipsoidal |
| 21 | [Geometry](#geometry) | 3 | Graham Scan, Jarvis March |
| 22 | [Graphs](#graphs) | 57 | Dijkstra, A*, Tarjan, PageRank |
| 23 | [Greedy Methods](#greedy-methods) | 9 | Fractional Knapsack, Gas Station |
| 24 | [Hashes](#hashes) | 12 | MD5, SHA-1, SHA-256, Luhn |
| 25 | [Knapsack](#knapsack) | 3 | 0/1, Fractional, Recursive |
| 26 | [Linear Algebra](#linear-algebra) | 13 | Gaussian, LU, QR, Power Iteration |
| 27 | [Linear Programming](#linear-programming) | 1 | Simplex Method |
| 28 | [Machine Learning](#machine-learning) | 31 | KNN, SVM, XGBoost, LSTM |
| 29 | [Maths](#maths) | 125 | Primes, FFT, Statistics, Number Theory |
| 30 | [Matrix](#matrix) | 21 | Strassen, Pascal, Spiral, Sudoku |
| 31 | [Networking Flow](#networking-flow) | 2 | Ford-Fulkerson, Min Cut |
| 32 | [Neural Network](#neural-network) | 5 | Backprop, CNN, MLP |
| 33 | [Other](#other) | 27 | LRU/LFU Cache, Tower of Hanoi, SDES |
| 34 | [Physics](#physics) | 34 | Orbital, Relativity, Thermodynamics |
| 35 | [Quantum](#quantum) | 1 | QFT (Quantum Fourier Transform) |
| 36 | [Scheduling](#scheduling) | 6 | FCFS, Round Robin, HRRN |
| 37 | [Searches](#searches) | 16 | Binary, Fibonacci, Tabu, A* |
| 38 | [Sorts](#sorts) | 47 | All major sorts + exotic variants |
| 39 | [Strings](#strings) | 52 | KMP, Rabin-Karp, Aho-Corasick |
| 40 | [Web Programming](#web-programming) | 33 | Scrapers, APIs, Crawlers |

---

## Audio Filters

Signal processing filters implemented in pure NumPy.

| Algorithm | Description | Complexity |
|-----------|-------------|------------|
| `butterworth_filter` | Low/high-pass IIR design | O(n) per sample |
| `iir_filter` | Generic infinite impulse response | O(n·k) |
| `show_response` | Frequency response visualization | O(n log n) |

---

## Backtracking

Constraint-satisfaction and combinatorial search via systematic backtracking.

| Algorithm | Description | Complexity |
|-----------|-------------|------------|
| `all_combinations` | Generate all k-combinations from n | O(C(n,k)) |
| `all_permutations` | All permutations of a sequence | O(n!) |
| `all_subsequences` | All 2ⁿ subsequences | O(2ⁿ) |
| `coloring` | Graph m-coloring problem | O(mⁿ) |
| `combination_sum` | All combos summing to target | O(2ⁿ) |
| `crossword_puzzle_solver` | Fill a crossword grid with words | O(n·m·k!) |
| `generate_parentheses` | All valid bracket sequences | O(4ⁿ/√n) |
| `hamiltonian_cycle` | Find Hamiltonian cycle in graph | O(n!) |
| `knight_tour` | Knight visits every chessboard square | O(8ⁿ) |
| `match_word_pattern` | Pattern-to-word bijective matching | O(n·m) |
| `minimax` | Game tree minimax with alpha-beta | O(bᵈ) |
| `n_queens` | Place N queens on N×N board | O(n!) |
| `n_queens_math` | Closed-form construction for N-Queens | O(n) |
| `power_sum` | Count ways to express X as sum of powers | O(X^(1/p)) |
| `rat_in_maze` | Find path in binary maze | O(2^(n²)) |
| `sudoku` | Solve 9×9 Sudoku via constraint prop | O(9^81) |
| `sum_of_subsets` | All subsets summing to target | O(2ⁿ) |
| `word_break` | Segment string using dictionary | O(n²) |
| `word_ladder` | BFS word transformation sequence | O(n·m²) |
| `word_search` | Find word in 2D letter grid | O(n·m·4^L) |

---

## Bit Manipulation

Bitwise tricks for O(1) solutions to classic problems.

| Algorithm | Key Trick | Complexity |
|-----------|-----------|------------|
| `binary_and_operator` | Bitwise AND from scratch | O(log n) |
| `binary_coded_decimal` | BCD ↔ integer conversion | O(d) |
| `binary_count_setbits` | Popcount via lookup/intrinsic | O(1) |
| `binary_count_trailing_zeros` | `n & -n` isolates lowest set bit | O(1) |
| `binary_or_operator` | Bitwise OR from scratch | O(log n) |
| `binary_shifts` | Arithmetic / logical shifts | O(1) |
| `binary_twos_complement` | `~n + 1` | O(log n) |
| `binary_xor_operator` | XOR from scratch | O(log n) |
| `bitwise_addition_recursive` | Add without `+` using XOR+carry | O(log n) |
| `count_1s_brian_kernighan_method` | `n &= n-1` clears lowest set bit | O(k) k=set bits |
| `count_number_of_one_bits` | Popcount 32-bit | O(1) |
| `excess_3_code` | XS-3 BCD encoding | O(d) |
| `find_previous_power_of_two` | `1 << floor(log2(n))` | O(1) |
| `find_unique_number` | XOR all — duplicates cancel | O(n) |
| `gray_code_sequence` | `n ^ (n >> 1)` | O(1) |
| `highest_set_bit` | `floor(log2(n))` position | O(1) |
| `index_of_rightmost_set_bit` | `log2(n & -n)` | O(1) |
| `is_even` | `n & 1 == 0` | O(1) |
| `is_power_of_two` | `n & (n-1) == 0` | O(1) |
| `largest_pow_of_two_le_num` | Bit smearing trick | O(1) |
| `missing_number` | XOR 0..n with array | O(n) |
| `numbers_different_signs` | `(a ^ b) < 0` | O(1) |
| `power_of_4` | `is_pow2 and n & 0xAAAA == 0` | O(1) |
| `reverse_bits` | 32-bit bit reversal | O(1) |
| `single_bit_manipulation_operations` | Get/set/clear/toggle bit | O(1) |
| `swap_all_odd_and_even_bits` | `(n & 0xAA) >> 1 | (n & 0x55) << 1` | O(1) |

---

## Boolean Algebra

Logic gates and minimization algorithms.

| Algorithm | Description |
|-----------|-------------|
| `and_gate` / `or_gate` / `not_gate` | Fundamental logic gates |
| `nand_gate` / `nor_gate` / `xor_gate` / `xnor_gate` | Secondary gates |
| `imply_gate` / `nimply_gate` | Implication gates |
| `multiplexer` | 2-to-1 MUX implementation |
| `karnaugh_map_simplification` | 2/3/4-variable K-map minimization |
| `quine_mc_cluskey` | Tabular Boolean minimization |

---

## Cellular Automata

Discrete dynamical systems on grids.

| Algorithm | Rules | Complexity |
|-----------|-------|------------|
| `conways_game_of_life` | Birth/survival rules B3/S23 | O(n·m) per step |
| `game_of_life` | Numpy-accelerated variant | O(n·m) per step |
| `langtons_ant` | 2-state Turing-complete ant | O(steps) |
| `nagel_schrekenberg` | Traffic flow simulation | O(n) per step |
| `one_dimensional` | Wolfram elementary CA (rule 30/90/…) | O(n) per gen |
| `wa_tor` | Predator-prey ocean simulation | O(n·m) per step |

---

## Ciphers

Classical and modern cryptography — pure Python, no external crypto libs.

### Substitution Ciphers
| Algorithm | Key Size | Notes |
|-----------|----------|-------|
| `caesar_cipher` | 1–25 (shift) | ROT-N, brute-forceable |
| `rot13` | Fixed (13) | Self-inverse |
| `atbash` | None | Alphabet reversal |
| `affine_cipher` | (a, b) | ax + b mod 26; gcd(a,26)=1 |
| `vigenere_cipher` | Variable string | Periodic polyalphabetic |
| `autokey` | Keyword + plaintext | Non-periodic Vigenère |
| `beaufort_cipher` | Variable string | Reciprocal Vigenère |
| `gronsfeld_cipher` | Digit string | Vigenère with digits |
| `running_key_cipher` | Long key text | True polyalphabetic |
| `playfair_cipher` | 5×5 keyword grid | Digraph substitution |
| `a1z26` | None | A=1, B=2, … |
| `baconian_cipher` | None | 5-bit binary encoding |
| `porta_cipher` | Variable | Bellaso's reciprocal table |
| `trifid_cipher` | 5×5×5 cube | 3D Polybius |
| `bifid` | 5×5 Polybius | Fractionate & recombine |
| `polybius` | 5×5 grid | Coordinate substitution |

### Transposition Ciphers
| Algorithm | Method |
|-----------|--------|
| `rail_fence_cipher` | Zigzag pattern |
| `transposition_cipher` | Columnar transposition |
| `permutation_cipher` | Keyed column permutation |

### Encoding / Base Conversions
| Algorithm | Encoding |
|-----------|---------|
| `base16` | Hex encoding |
| `base32` | RFC 4648 Base-32 |
| `base64_cipher` | RFC 4648 Base-64 |
| `base85` | ASCII-85 (PDF/PostScript) |

### Stream / XOR Ciphers
| Algorithm | Notes |
|-----------|-------|
| `xor_cipher` | Single-key XOR |
| `vernam_cipher` | One-time pad (XOR) |
| `onepad_cipher` | True OTP — information-theoretically secure |

### Public Key Cryptography
| Algorithm | Security Basis | Notes |
|-----------|---------------|-------|
| `rsa_cipher` | Integer factorization | PKCS#1 style |
| `rsa_key_generator` | Generate p, q, e, d | Textbook RSA |
| `rsa_factorization` | Fermat's factorization attack | Breaks weak keys |
| `diffie_hellman` | Discrete log (DH) | Key exchange |
| `elgamal_key_generator` | Discrete log (ElGamal) | Public key gen |
| `rabin_miller` | Miller-Rabin primality | Probabilistic |
| `deterministic_miller_rabin` | Deterministic for n < 3.3×10²⁴ | Deterministic |

### Other Ciphers
| Algorithm | Type |
|-----------|------|
| `enigma_machine2` | Rotor substitution machine |
| `hill_cipher` | Linear algebra (matrix key) |
| `morse_code` | International Morse |
| `fractionated_morse_cipher` | Morse + Polybius |
| `mono_alphabetic_ciphers` | Single-alphabet substitution |
| `mixed_keyword_cypher` | Keyword-shifted alphabet |
| `simple_keyword_cypher` | Keyword prepend cipher |
| `simple_substitution_cipher` | Full alphabet permutation |
| `brute_force_caesar_cipher` | Exhaustive 1–25 search |
| `decrypt_caesar_with_chi_squared` | χ² frequency analysis |
| `shuffled_shift_cipher` | Random seeded shift |
| `cryptomath_module` | GCD, modular inverse helpers |
| `diffie` | Primitive root finder |

---

## Computer Vision

| Algorithm | Method | Use Case |
|-----------|--------|---------|
| `cnn_classification` | Convolutional feature maps | Image classification |
| `flip_augmentation` | Horizontal/vertical flip | Data augmentation |
| `haralick_descriptors` | GLCM texture features | Texture analysis |
| `harris_corner` | Second moment matrix | Corner detection |
| `horn_schunck` | Variational optical flow | Motion estimation |
| `intensity_based_segmentation` | Threshold + morphology | Region segmentation |
| `mean_threshold` | Adaptive mean thresholding | Binarization |
| `mosaic_augmentation` | 4-image mosaic | YOLOv4-style augment |
| `pooling_functions` | Max/avg/min pool | CNN downsampling |

---

## Conversions

| Algorithm | Converts |
|-----------|---------|
| `binary_to_decimal` / `decimal_to_binary` | Binary ↔ Decimal |
| `binary_to_hexadecimal` / `hex_to_bin` | Binary ↔ Hex |
| `binary_to_octal` / `octal_to_binary` | Binary ↔ Octal |
| `decimal_to_hexadecimal` / `hexadecimal_to_decimal` | Hex ↔ Decimal |
| `decimal_to_octal` / `octal_to_decimal` | Octal ↔ Decimal |
| `octal_to_hexadecimal` | Octal → Hex |
| `decimal_to_any` | Decimal → any base (2–36) |
| `convert_number_to_words` | 123 → "one hundred twenty-three" |
| `roman_numerals` | Roman ↔ Integer |
| `excel_title_to_column` | "AA" → 27 |
| `prefix_conversions` | kilo/mega/giga… numeric |
| `ipv4_conversion` | IPv4 ↔ integer |
| `rgb_cmyk_conversion` | RGB ↔ CMYK |
| `rgb_hsv_conversion` | RGB ↔ HSV |
| `rectangular_to_polar` | (x,y) ↔ (r,θ) |
| `molecular_chemistry` | Molar mass, composition |
| `astronomical_length_scale_conversion` | AU/ly/pc |
| `length_conversion` | m/ft/in/mi/… |
| `speed_conversions` | m/s, km/h, mph, knots |
| `temperature_conversions` | C/F/K/R |
| `pressure_conversions` | Pa/atm/psi/bar |
| `volume_conversions` | L/gal/ft³/… |
| `weight_conversion` | kg/lb/oz/… |
| `energy_conversions` | J/cal/BTU/eV |
| `time_conversions` | s/min/hr/day/… |

---

## Data Compression

| Algorithm | Type | Ratio | Complexity |
|-----------|------|-------|------------|
| `huffman` | Entropy / lossless | Variable | O(n log n) build |
| `run_length_encoding` | Lossless | Up to n:1 on runs | O(n) |
| `lempel_ziv` | Dictionary / LZ78 | Good on repetition | O(n) |
| `lempel_ziv_decompress` | LZ78 decompressor | — | O(n) |
| `lz77` | Sliding window / LZ77 | Better than LZ78 | O(n·w) |
| `burrows_wheeler` | BWT transform | Preprocessing for BWT-MTF | O(n log n) |
| `coordinate_compression` | Rank compression | — | O(n log n) |
| `peak_signal_to_noise_ratio` | PSNR quality metric | — | O(n·m) |

---

## Data Structures

All files are flat in `data_structures/` with category prefix naming.

### Arrays
| Algorithm | Complexity |
|-----------|------------|
| `arrays_equilibrium_index_in_array` | O(n) single-pass prefix sum |
| `arrays_kth_largest_element` | O(n) avg (QuickSelect) |
| `arrays_monotonic_array` | O(n) |
| `arrays_prefix_sum` | O(n) build, O(1) query |
| `arrays_product_sum` | O(n) recursive depth-weighted |

### Binary Trees
| Algorithm | Type | Complexity |
|-----------|------|------------|
| `binary_tree_avl_tree` | Self-balancing BST | O(log n) insert/search |
| `binary_tree_binary_search_tree` | BST (iterative) | O(log n) avg, O(n) worst |
| `binary_tree_binary_search_tree_recursive` | BST (recursive) | O(log n) avg |
| `binary_tree_binary_tree_traversals` | All 6 traversals + Morris | O(n) |
| `binary_tree_diameter_of_binary_tree` | Single-pass DFS | O(n) |
| `binary_tree_fenwick_tree` | BIT / Fenwick | O(log n) update/query |
| `binary_tree_maximum_fenwick_tree` | Max-BIT variant | O(log n) |
| `binary_tree_lazy_segment_tree` | Range assign + range max | O(log n) |
| `binary_tree_segment_tree` | Recursive range max | O(log n) |
| `binary_tree_non_recursive_segment_tree` | Iterative segment tree | O(log n) |
| `binary_tree_lowest_common_ancestor` | Binary lifting sparse table | O(n log n) build, O(log n) query |
| `binary_tree_red_black_tree` | RBT insert/delete/floor/ceil | O(log n) |
| `binary_tree_treap` | Randomized BST split/merge | O(log n) expected |
| `binary_tree_wavelet_tree` | Rank/quantile/range count | O(n log n) build, O(log n) query |
| `binary_tree_serialize_deserialize_binary_tree` | Preorder string encoding | O(n) |
| `binary_tree_lowest_common_ancestor` | LCA via binary lifting | O(log n) |
| `binary_tree_number_of_possible_binary_trees` | Catalan number Cₙ | O(n) |
| `binary_tree_maximum_sum_bst` | Max sum BST subtree | O(n) |
| `binary_tree_symmetric_tree` | Mirror symmetry check | O(n) |

### Heaps
| Algorithm | Type | Extract | Insert |
|-----------|------|---------|--------|
| `heap_min_heap` | Binary min-heap | O(log n) | O(log n) |
| `heap_max_heap` | Binary max-heap | O(log n) | O(log n) |
| `heap_heap_generic` | Generic comparator heap | O(log n) | O(log n) |
| `heap_binomial_heap` | Binomial heap | O(log n) | O(1) amortized |
| `heap_skew_heap` | Leftist/skew merge | O(log n) | O(log n) |
| `heap_randomized_heap` | Randomized meldable | O(log n) expected | O(log n) |

### Hash Tables
| Algorithm | Collision Strategy |
|-----------|-------------------|
| `hashing_hash_table` | Open addressing (linear) |
| `hashing_double_hash` | Double hashing |
| `hashing_quadratic_probing` | Quadratic probing |
| `hashing_hash_table_with_linked_list` | Separate chaining |
| `hashing_bloom_filter` | Probabilistic set membership |

### Linked Lists
| Algorithm | Type |
|-----------|------|
| `linked_list_singly_linked_list` | Singly linked (head + tail) |
| `linked_list_doubly_linked_list` | Doubly linked |
| `linked_list_circular_linked_list` | Circular singly linked |
| `linked_list_deque_doubly` | Deque via doubly linked |
| `linked_list_skip_list` | Probabilistic O(log n) search |
| `linked_list_is_palindrome` | Two-pointer check |
| `linked_list_has_loop` | Floyd's cycle detection |
| `linked_list_reverse_k_group` | Reverse in groups of k |
| `linked_list_middle_element_of_linked_list` | Slow/fast pointer |

### Queues
| Algorithm | Notes |
|-----------|-------|
| `queues_queue_by_list` | O(n) dequeue — simple |
| `queues_queue_by_two_stacks` | Amortized O(1) |
| `queues_circular_queue` | Fixed capacity ring buffer |
| `queues_double_ended_queue` | Deque (both ends O(1)) |
| `queues_priority_queue_using_list` | O(n) insert, O(1) extract |
| `queues_linked_queue` | Pointer-based unbounded |

### Stacks
| Algorithm | Notes |
|-----------|-------|
| `stacks_stack` | List-backed push/pop O(1) |
| `stacks_balanced_parentheses` | `()[]{}` validation O(n) |
| `stacks_infix_to_postfix_conversion` | Shunting-yard O(n) |
| `stacks_infix_to_prefix_conversion` | Reverse shunting-yard |
| `stacks_postfix_evaluation` | RPN evaluator O(n) |
| `stacks_next_greater_element` | Monotonic stack O(n) |
| `stacks_stock_span_problem` | Monotonic stack O(n) |
| `stacks_dijkstras_two_stack_algorithm` | Expression evaluator |

### Trees & Tries
| Algorithm | Notes |
|-----------|-------|
| `kd_tree_build_kdtree` | k-d tree construction O(n log n) |
| `kd_tree_nearest_neighbour_search` | NN query O(log n) avg |
| `trie_trie` | Character prefix trie |
| `trie_radix_tree` | Compressed trie |
| `suffix_tree_suffix_tree` | Ukkonen-style suffix tree |

### Disjoint Sets
| Algorithm | Notes |
|-----------|-------|
| `disjoint_set_disjoint_set` | Union-Find + path compression + union by rank → O(α(n)) |
| `disjoint_set_alternate_disjoint_set` | Array-based with set size tracking |

---

## Digital Image Processing

Flat files with category prefix in `digital_image_processing/`.

| Category | Algorithms |
|----------|-----------|
| **Edge Detection** | Canny, Sobel, Prewitt, Roberts cross |
| **Filters** | Bilateral, Gaussian blur, Median, Mean |
| **Morphology** | Erosion, Dilation, Opening, Closing |
| **Transformation** | Histogram equalization, Contrast stretch |

---

## Divide & Conquer

| Algorithm | Problem | Complexity |
|-----------|---------|------------|
| `closest_pair_of_points` | Min distance between n points | O(n log n) |
| `convex_hull` | Divide & conquer hull | O(n log n) |
| `heaps_algorithm` | All permutations | O(n!) |
| `heaps_algorithm_iterative` | Iterative Heap's algorithm | O(n!) |
| `inversions` | Count inversions in array | O(n log n) |
| `kth_order_statistic` | kth smallest (D&C QuickSelect) | O(n) avg |
| `max_difference_pair` | Max a[j]-a[i] with j>i | O(n) |
| `max_subarray` | Kadane's / D&C max subarray | O(n) / O(n log n) |
| `mergesort` | D&C merge sort | O(n log n) |
| `peak` | Find local peak in array | O(log n) |
| `power` | Fast exponentiation | O(log n) |
| `strassen_matrix_multiplication` | Strassen's matrix multiply | O(n^2.807) |

---

## Dynamic Programming

| Algorithm | Complexity | Notes |
|-----------|------------|-------|
| `abbreviation` | O(n·m) | String abbreviation matching |
| `all_construct` | O(n·w) | All ways to build string from dict |
| `bitmask` | O(n·2ⁿ) | Bitmask DP template |
| `catalan_numbers` | O(n) | Catalan number sequence |
| `climbing_stairs` | O(n) | Fibonacci-style DP |
| `combination_sum_iv` | O(target·n) | Ordered combination count |
| `edit_distance` | O(n·m) | Levenshtein / Wagner-Fischer |
| `fibonacci` | O(n) | Bottom-up tabulation |
| `fast_fibonacci` | O(log n) | Matrix exponentiation |
| `floyd_warshall` | O(V³) | All-pairs shortest paths |
| `integer_partition` | O(n²) | Partition function p(n) |
| `knapsack` | O(n·W) | 0/1 knapsack |
| `largest_divisible_subset` | O(n²) | Longest chain of divisors |
| `longest_common_subsequence` | O(n·m) | LCS with reconstruction |
| `longest_common_substring` | O(n·m) | Contiguous LCS |
| `longest_increasing_subsequence` | O(n log n) | patience sort / binary search |
| `longest_palindromic_subsequence` | O(n²) | Expand around center |
| `matrix_chain_multiplication` | O(n³) | Optimal parenthesization |
| `max_product_subarray` | O(n) | Track min/max simultaneously |
| `max_subarray_sum` | O(n) | Kadane's algorithm |
| `minimum_coin_change` | O(n·C) | Bottom-up coin DP |
| `minimum_cost_path` | O(n·m) | Grid path cost |
| `minimum_partition` | O(n·sum) | Partition into equal sum halves |
| `minimum_squares_to_represent_a_number` | O(n·√n) | Lagrange four-square |
| `optimal_binary_search_tree` | O(n³) | Knuth's OBST construction |
| `palindrome_partitioning` | O(n²) | Min cuts for palindrome parts |
| `range_sum_query` | O(1) query | 2D prefix sum |
| `regex_match` | O(n·m) | Regex `.` and `*` matching |
| `rod_cutting` | O(n²) | Max revenue from rod cuts |
| `smith_waterman` | O(n·m) | Local sequence alignment |
| `subset_generation` | O(2ⁿ) | All subsets via bitmask |
| `sum_of_subset` | O(n·sum) | Subset sum existence |
| `trapped_water` | O(n) | Two-pointer water trapping |
| `tribonacci` | O(n) | T(n) = T(n-1)+T(n-2)+T(n-3) |
| `viterbi` | O(n·m²) | HMM most likely path |
| `wildcard_matching` | O(n·m) | `?` and `*` pattern matching |
| `word_break` | O(n²·d) | String segmentation with dict |

---

## Electronics

| Algorithm | Domain |
|-----------|--------|
| `ohms_law` | V = IR — solve for any variable |
| `electric_power` | P = VI = I²R = V²/R |
| `electrical_impedance` | Complex Z = R + jX |
| `coulombs_law` | F = kq₁q₂/r² |
| `electric_conductivity` | σ = 1/ρ |
| `ind_reactance` | X_L = 2πfL |
| `real_and_reactive_power` | S = P + jQ |
| `apparent_power` | |S| = √(P²+Q²) |
| `resonant_frequency` | f = 1/(2π√LC) |
| `wheatstone_bridge` | Null-detector bridge |
| `resistor_equivalence` | Series / parallel |
| `capacitor_equivalence` | Series / parallel |
| `charging_capacitor` | V(t) = V₀(1 − e^(−t/RC)) |
| `charging_inductor` | I(t) = (V/R)(1 − e^(−Rt/L)) |
| `circular_convolution` | DFT-based convolution |
| `ic_555_timer` | Astable / monostable timing |
| `builtin_voltage` | p-n junction built-in potential |
| `carrier_concentration` | Semiconductor n·p = nᵢ² |
| `resistor_color_code` | 4/5-band resistor decoding |

---

## Financial

| Algorithm | Formula |
|-----------|---------|
| `equated_monthly_installments` | EMI = P·r(1+r)ⁿ / ((1+r)ⁿ−1) |
| `simple_moving_average` | SMA(k) rolling window |
| `exponential_moving_average` | EMA with α = 2/(k+1) |
| `interest` | Simple & compound interest |
| `present_value` | PV = FV / (1+r)ⁿ |
| `price_plus_tax` | Gross price calculation |
| `straight_line_depreciation` | (Cost − Salvage) / Life |
| `time_and_half_pay` | Overtime 1.5× calculation |

---

## Fractals

| Algorithm | Dimension | Notes |
|-----------|-----------|-------|
| `mandelbrot` | ~2.0 | Escape-time coloring |
| `julia_sets` | Variable | Parameter c variants |
| `koch_snowflake` | log4/log3 ≈ 1.26 | Recursive subdivision |
| `sierpinski_triangle` | log3/log2 ≈ 1.585 | Chaos game / recursive |
| `vicsek` | log5/log3 ≈ 1.465 | Cross-shaped fractal |

---

## Geodesy

| Algorithm | Formula | Error |
|-----------|---------|-------|
| `haversine_distance` | Spherical law of cosines | <0.3% (ignores oblateness) |
| `lamberts_ellipsoidal_distance` | WGS-84 Vincenty iterate | ~0.5mm accuracy |

---

## Geometry

| Algorithm | Problem | Complexity |
|-----------|---------|------------|
| `graham_scan` | Convex hull | O(n log n) |
| `jarvis_march` | Convex hull (gift wrapping) | O(n·h) h=hull points |
| `geometry` | Point/line/polygon primitives | O(1)–O(n) |

---

## Graphs

### Shortest Paths
| Algorithm | Graph Type | Complexity |
|-----------|-----------|------------|
| `dijkstra` | Weighted, non-negative | O((V+E) log V) |
| `dijkstra_alternate` | Binary heap variant | O((V+E) log V) |
| `dijkstra_binary_grid` | 0-1 BFS on grid | O(V+E) |
| `bellman_ford` | Negative weights OK | O(V·E) |
| `graphs_floyd_warshall` | All-pairs | O(V³) |
| `a_star` | Heuristic guided | O(E log V) |
| `bidirectional_a_star` | Bi-directional A* | O(b^(d/2)) |
| `bi_directional_dijkstra` | Bidirectional Dijkstra | O(E log V) |
| `minimum_path_sum` | Grid DP | O(n·m) |

### Minimum Spanning Tree
| Algorithm | Strategy | Complexity |
|-----------|---------|------------|
| `minimum_spanning_tree_kruskal` | Union-Find on edges | O(E log E) |
| `minimum_spanning_tree_prims` | Priority queue | O(E log V) |
| `minimum_spanning_tree_boruvka` | Borůvka's parallel MST | O(E log V) |
| `prim` | Prim's variant | O(E log V) |

### Graph Traversal
| Algorithm | Notes |
|-----------|-------|
| `breadth_first_search` | Queue-based BFS |
| `depth_first_search` | Stack / recursive DFS |
| `bidirectional_breadth_first_search` | Meet-in-middle BFS |

### Connectivity & Components
| Algorithm | Problem | Complexity |
|-----------|---------|------------|
| `connected_components` | Undirected CC via DFS/BFS | O(V+E) |
| `scc_kosaraju` | Strongly connected components | O(V+E) |
| `tarjans_scc` | Tarjan's SCC (one DFS) | O(V+E) |
| `strongly_connected_components` | Variant | O(V+E) |
| `articulation_points` | Bridge/cut vertices | O(V+E) |
| `finding_bridges` | Bridge edges | O(V+E) |
| `eulerian_path_and_circuit_for_undirected_graph` | Hierholzer's | O(E) |

### Topological Sort & DAG
| Algorithm | Notes |
|-----------|-------|
| `g_topological_sort` | DFS-based topo sort |
| `kahns_algorithm_topo` | Kahn's BFS-based |
| `kahns_algorithm_long` | Longest path in DAG |
| `check_cycle` | Detect cycle (directed/undirected) |

### Other Graph Algorithms
| Algorithm | Problem | Complexity |
|-----------|---------|------------|
| `page_rank` | Iterative rank propagation | O(V+E) per iter |
| `markov_chain` | Steady-state distribution | O(V²) per step |
| `karger` | Min-cut via contraction | O(V²·E) |
| `gale_shapley_bigraph` | Stable matching | O(V²) |
| `check_bipatrite` | 2-coloring check | O(V+E) |
| `greedy_min_vertex_cover` | 2-approx vertex cover | O(V+E) |
| `matching_min_vertex_cover` | König's theorem | O(V+E) |
| `greedy_best_first` | Greedy best-first search | O(b^m) |
| `ant_colony_optimization_algorithms` | ACO pheromone trail | O(iter·ants·n²) |
| `frequent_pattern_graph_miner` | Graph pattern mining | — |
| `lanczos_eigenvectors` | Sparse eigenvalue solver | O(k·n) |

---

## Greedy Methods

| Algorithm | Greedy Choice | Complexity |
|-----------|--------------|------------|
| `fractional_knapsack` | Highest value/weight ratio first | O(n log n) |
| `fractional_cover_problem` | Min-cost cover | O(n log n) |
| `gas_station` | Start where surplus > 0 | O(n) |
| `minimum_coin_change` | Largest coin first (canonical systems) | O(n) |
| `minimum_waiting_time` | Sort by burst time | O(n log n) |
| `optimal_merge_pattern` | Min-cost merge (Huffman-like) | O(n log n) |
| `best_time_to_buy_and_sell_stock` | Track running min | O(n) |
| `fractional_knapsack_2` | Alternative heap-based | O(n log n) |
| `smallest_range` | Sliding window on sorted lists | O(n log k) |

---

## Hashes

| Algorithm | Output | Notes |
|-----------|--------|-------|
| `md5` | 128-bit | Cryptographically broken, fast |
| `sha1` | 160-bit | Deprecated for security |
| `sha256` | 256-bit | Current standard |
| `adler32` | 32-bit | Fast checksum (zlib) |
| `fletcher16` | 16-bit | Better than simple sum |
| `djb2` | 32-bit | String hashing |
| `sdbm` | 32-bit | SDBM database hash |
| `elf` | 32-bit | ELF binary hash |
| `luhn` | 1-bit | Credit card checksum |
| `hamming_code` | Variable | Error detection/correction |
| `chaos_machine` | Variable | PRNG-based hash |
| `enigma_machine` | — | Hash demo using Enigma |

---

## Linear Algebra

| Algorithm | Solves | Complexity |
|-----------|--------|------------|
| `gaussian_elimination` | Ax = b (no pivoting) | O(n³) |
| `gaussian_elimination_pivoting` | Ax = b (partial pivot) | O(n³) |
| `lu_decomposition` | LU factorization | O(n³) |
| `conjugate_gradient` | Sparse symmetric Ax = b | O(k·n²) |
| `jacobi_iteration_method` | Iterative Ax = b | O(k·n²) |
| `power_iteration` | Dominant eigenvector | O(k·n²) |
| `rayleigh_quotient` | Eigenvalue refinement | O(n²) |
| `matrix_inversion` | A⁻¹ via Gauss-Jordan | O(n³) |
| `schur_complement` | Block matrix inversion | O(n³) |
| `qr_decomposition` | QR factorization | O(n³) |
| `polynom_for_points` | Lagrange interpolation | O(n²) |
| `rank_of_matrix` | Row echelon rank | O(n³) |
| `transformations_2d` | Rotation/scale/shear | O(1) |

---

## Machine Learning

| Algorithm | Type | Notes |
|-----------|------|-------|
| `linear_regression` | Supervised | Normal equation + gradient descent |
| `logistic_regression` | Supervised | Sigmoid + log-loss |
| `decision_tree` | Supervised | ID3 / CART, Gini impurity |
| `k_nearest_neighbours` | Supervised | Euclidean distance, k=1..n |
| `support_vector_machines` | Supervised | Sequential minimal optimization |
| `gradient_boosting_classifier` | Ensemble | Residual-based boosting |
| `xgboost_classifier` / `xgboost_regressor` | Ensemble | Regularized boosting |
| `k_means_clust` | Unsupervised | Lloyd's algorithm |
| `principle_component_analysis` | Dim. reduction | SVD-based |
| `linear_discriminant_analysis` | Supervised dim. red. | Fisher's LDA |
| `t_stochastic_neighbour_embedding` | Visualization | t-SNE |
| `self_organizing_map` | Unsupervised | Kohonen SOM |
| `multilayer_perceptron_classifier` | Neural | Backprop MLP |
| `polynomial_regression` | Regression | Vandermonde matrix |
| `local_weighted_learning` | Non-parametric | LOWESS / Nadaraya-Watson |
| `gradient_descent` | Optimization | SGD, mini-batch, adaptive |
| `loss_functions` | Reference | MSE, MAE, BCE, Huber |
| `scoring_functions` | Reference | Accuracy, F1, AUC |
| `automatic_differentiation` | AD | Forward-mode dual numbers |
| `sequential_minimum_optimization` | SVM solver | Platt's SMO |
| `lstm_prediction` | RNN | LSTM time-series |
| `mfcc` | Feature extraction | Mel-frequency cepstrum |
| `word_frequency_functions` | NLP | TF-IDF, bag-of-words |
| `similarity_search` | Retrieval | Cosine, L2 similarity |
| `apriori_algorithm` | Association rules | Support/confidence mining |
| `frequent_pattern_growth` | Association rules | FP-tree, no candidate gen |
| `dimensionality_reduction` | Reference | PCA, LDA, t-SNE compared |
| `data_transformations` | Preprocessing | Normalize, standardize, encode |
| `forecasting_run` | Time series | Moving avg, exponential smooth |

---

## Maths

### Number Theory
| Algorithm | Problem | Complexity |
|-----------|---------|------------|
| `prime_check` | Primality test | O(√n) |
| `prime_sieve_eratosthenes` / `sieve_of_eratosthenes` | Primes up to n | O(n log log n) |
| `prime_factors` | Integer factorization | O(√n) |
| `germain_primes` | Safe primes p, 2p+1 | O(√n) per prime |
| `segmented_sieve` | Memory-efficient sieve | O(n log log n), O(√n) space |
| `pollard_rho` | Fast factorization | O(n^(1/4)) expected |
| `extended_euclidean_algorithm` | GCD + Bézout coeffs | O(log min(a,b)) |
| `eulers_totient` | φ(n) Euler's totient | O(√n) |
| `modular_division` | a/b mod m | O(log m) |
| `modular_exponential` | aᵇ mod m | O(log b) |
| `fermat_little_theorem` | aᵖ⁻¹ ≡ 1 (mod p) | O(log p) |
| `chinese_remainder_theorem` | CRT system of congruences | O(n log M) |
| `twin_prime` | Twin prime pairs | O(√n) |
| `liouville_lambda` | Liouville λ function | O(√n) |
| `mobius_function` | Möbius μ function | O(√n) |

### Sequences & Series
| Algorithm | Notes |
|-----------|-------|
| `fibonacci` | Memoized / tabulated / matrix |
| `collatz_sequence` | 3n+1 conjecture trace |
| `lucas_series` | L(n) = L(n-1) + L(n-2), L(0)=2 |
| `sylvester_sequence` | a₀=2, aₙ=a₀·…·aₙ₋₁+1 |
| `juggler_sequence` | √n up, n^(3/2) down |
| `sum_of_arithmetic_series` | n(a₁+aₙ)/2 |
| `sum_of_geometric_progression` | a(rⁿ−1)/(r−1) |
| `sum_of_harmonic_series` | H(n) ≈ ln(n) + γ |

### Combinatorics
| Algorithm | Formula |
|-----------|---------|
| `binomial_coefficient` | C(n,k) — Pascal / DP |
| `combinations` | All k-subsets enumeration |
| `kth_lexicographic_permutation` | Factoradic decode |
| `integer_square_root` | Newton's method integer √ |
| `double_factorial` | n!! = n·(n-2)·… |
| `josephus_problem` | Survivor in circular elimination |

### Pi & Constants
| Algorithm | Method | Digits |
|-----------|--------|--------|
| `pi_monte_carlo_estimation` | Monte Carlo | O(n) for n samples |
| `pi_generator` | Leibniz series | Slow convergence |
| `chudnovsky_algorithm` | Ramanujan-style | ~14 digits per term |
| `bailey_borwein_plouffe` | BBP formula | Direct nth hex digit |

### Statistics & Distance
| Algorithm | Formula |
|-----------|---------|
| `average_mean` / `average_median` / `average_mode` | Descriptive stats |
| `average_absolute_deviation` | MAD |
| `interquartile_range` | IQR = Q3 − Q1 |
| `spearman_rank_correlation_coefficient` | Rank correlation |
| `jaccard_similarity` | |A∩B| / |A∪B| |
| `gaussian` | Normal PDF |
| `softmax` | Stable softmax |
| `sigmoid` | 1/(1+e^−x) |
| `manhattan_distance` | Σ|xᵢ−yᵢ| |
| `euclidean_distance` | √Σ(xᵢ−yᵢ)² |
| `chebyshev_distance` | max|xᵢ−yᵢ| |
| `minkowski_distance` | (Σ|xᵢ−yᵢ|ᵖ)^(1/p) |

### Numerical Methods
| Algorithm | Method |
|-----------|--------|
| `euler_method` | ODE solver y' = f(x,y) |
| `euler_modified` | Heun's method (improved Euler) |
| `trapezoidal_rule` | Numerical integration |
| `area_under_curve` | Simpson's 1/3 rule |
| `newton_method` (via `basic_maths`) | Root finding |
| `continued_fraction` | Rational approximations |
| `maclaurin_series` | Taylor expansion at 0 |

### Transforms
| Algorithm | Domain |
|-----------|--------|
| `radix2_fft` | Cooley-Tukey FFT O(n log n) |
| `binary_exponentiation` | Fast pow O(log n) |
| `binary_multiplication` | Peasant multiplication |
| `karatsuba` | Multiply in O(n^1.585) |
| `matrix_exponentiation` | Matrix fast pow O(k³ log n) |
| `qr_decomposition` | QR factorization |
| `dual_number_automatic_differentiation` | Forward-mode AD |

---

## Matrix

| Algorithm | Notes | Complexity |
|-----------|-------|------------|
| `matrix_operation` | Add, subtract, multiply, transpose | O(n²)–O(n³) |
| `matrix_class` | Full OOP matrix with all ops | O(n²)–O(n³) |
| `matrix_multiplication_recursion` | D&C Strassen-style | O(n^2.807) |
| `inverse_of_matrix` | Gauss-Jordan elimination | O(n³) |
| `cramers_rule_2x2` | 2×2 linear system | O(1) |
| `sherman_morrison` | Rank-1 update of A⁻¹ | O(n²) |
| `rotate_matrix` | 90°/180°/270° in-place | O(n²) |
| `spiral_print` | Layer-by-layer traversal | O(n·m) |
| `pascal_triangle` | Row-by-row construction | O(n²) |
| `nth_fibonacci_using_matrix_exponentiation` | Matrix fast Fibonacci | O(log n) |
| `count_paths` | DP path counting in grid | O(n·m) |
| `largest_square_area_in_matrix` | Maximal square DP | O(n·m) |
| `max_area_of_island` | DFS island area | O(n·m) |
| `count_islands_in_matrix` | DFS/BFS flood fill | O(n·m) |
| `binary_search_matrix` | Search in sorted matrix | O(log(n·m)) |
| `searching_in_sorted_matrix` | Staircase search | O(n+m) |
| `count_negative_numbers_in_sorted_matrix` | Binary search per row | O(n log m) |
| `median_matrix` | Binary search on value | O(n·m·log(max)) |
| `validate_sudoku_board` | Set-based row/col/box check | O(1) (9×9) |
| `matrix_based_game` | 2D board game logic | O(n·m) |
| `matrix_equalization` | Equalize columns efficiently | O(n·m) |

---

## Networking Flow

| Algorithm | Problem | Complexity |
|-----------|---------|------------|
| `ford_fulkerson` | Max flow (DFS augmentation) | O(E · max_flow) |
| `minimum_cut` | Min s-t cut via max-flow | O(V·E²) |

---

## Neural Network

| Algorithm | Architecture |
|-----------|-------------|
| `simple_neural_network` | Single layer perceptron |
| `back_propagation_neural_network` | Multi-layer with backprop |
| `two_hidden_layers_neural_network` | 3-layer MLP |
| `convolution_neural_network` | Conv + Pool + Dense |
| `input_data` | Data loading / normalization |

---

## Other

| Algorithm | Category |
|-----------|---------|
| `lru_cache` | Least Recently Used cache (O(1) get/put) |
| `lfu_cache` | Least Frequently Used cache (O(1)) |
| `least_recently_used` | LRU via OrderedDict |
| `tower_of_hanoi` | Classic recursion (2ⁿ−1 moves) |
| `bankers_algorithm` | Deadlock avoidance |
| `davis_putnam_logemann_loveland` | DPLL SAT solver |
| `majority_vote_algorithm` | Boyer-Moore voting O(n) |
| `sliding_window_maximum` | Monotonic deque O(n) |
| `maximum_subsequence` | O(n) max product subsequence |
| `nested_brackets` | Bracket depth counter |
| `h_index` | Hirsch citation index |
| `password` | Password strength checker |
| `linear_congruential_generator` | LCG PRNG |
| `fischer_yates_shuffle` | Knuth shuffle O(n) |
| `graham_scan` | Convex hull (duplicate) |
| `greedy` | Generic greedy template |
| `guess_the_number_search` | Binary search game |
| `doomsday` | Day of week for any date |
| `gauss_easter` | Gauss Easter algorithm |
| `sdes` | Simplified DES cipher |
| `quine` | Self-replicating program |
| `scoring_algorithm` | Scoring / ranking system |
| `number_container_system` | Number ↔ container mapping |
| `activity_selection` | Greedy interval scheduling |
| `alternative_list_arrange` | Interleave two lists |
| `magicdiamondpattern` | ASCII diamond pattern |
| `word_search` | 2D word board search |

---

## Physics

| Algorithm | Law / Formula |
|-----------|--------------|
| `newtons_second_law_of_motion` | F = ma |
| `newtons_law_of_gravitation` | F = Gm₁m₂/r² |
| `kinetic_energy` | KE = ½mv² |
| `potential_energy` | PE = mgh |
| `mass_energy_equivalence` | E = mc² |
| `escape_velocity` | v = √(2GM/r) |
| `orbital_transfer_work` | Hohmann transfer ΔV |
| `basic_orbital_capture` | Capture orbit mechanics |
| `hubble_parameter` | H(z) = H₀√(Ωm(1+z)³+ΩΛ) |
| `doppler_frequency` | f' = f·(v±vo)/(v∓vs) |
| `ideal_gas_law` | PV = nRT |
| `archimedes_principle_of_buoyant_force` | F_b = ρ·V·g |
| `centripetal_force` | F = mv²/r |
| `casimir_effect` | F = πhcA/(480d⁴) |
| `lorentz_transformation_four_vector` | Special relativity 4-vector |
| `speed_of_sound` | v = √(γRT/M) |
| `rms_speed_of_molecule` | v_rms = √(3RT/M) |
| `grahams_law` | Effusion rate ∝ 1/√M |
| `malus_law` | I = I₀cos²θ (polarization) |
| `photoelectric_effect` | E_k = hf − φ |
| `period_of_pendulum` | T = 2π√(L/g) |
| `horizontal_projectile_motion` | Range, height, time |
| `altitude_pressure` | P(h) = P₀e^(−Mgh/RT) |
| `reynolds_number` | Re = ρvL/μ |
| `shear_stress` | τ = F/A |
| `lens_formulae` | 1/f = 1/v − 1/u |
| `mirror_formulae` | 1/f = 1/v + 1/u |
| `in_static_equilibrium` | ΣF = 0, Στ = 0 |
| `rainfall_intensity` | I = Q/A |
| `terminal_velocity` | v_t = √(2mg/ρAC_d) |
| `n_body_simulation` | Leapfrog integration |
| `center_of_mass` | x_cm = Σmᵢxᵢ/Σmᵢ |
| `speeds_of_gas_molecules` | Maxwell-Boltzmann distribution |

---

## Quantum

| Algorithm | Circuit | Notes |
|-----------|---------|-------|
| `q_fourier_transform` | QFT | O(n²) gates, quantum speedup for phase estimation |

---

## Scheduling

| Algorithm | Strategy | Complexity |
|-----------|---------|------------|
| `first_come_first_served` | FIFO queue | O(n) |
| `round_robin` | Time-slice rotation | O(n·q) |
| `highest_response_ratio_next` | HRRN — (W+S)/S priority | O(n²) |
| `job_sequence_with_deadline` | Greedy deadline scheduling | O(n log n) |
| `job_sequencing_with_deadline` | DP variant | O(n²) |
| `multi_level_feedback_queue` | MLFQ with aging | O(n·q) |

---

## Searches

| Algorithm | Best Case | Average | Worst Case | Space |
|-----------|-----------|---------|------------|-------|
| `linear_search` | O(1) | O(n) | O(n) | O(1) |
| `binary_search` | O(1) | O(log n) | O(log n) | O(1) |
| `simple_binary_search` | O(1) | O(log n) | O(log n) | O(1) |
| `exponential_search` | O(1) | O(log n) | O(log n) | O(1) |
| `fibonacci_search` | O(1) | O(log n) | O(log n) | O(1) |
| `jump_search` | O(1) | O(√n) | O(√n) | O(1) |
| `ternary_search` | O(1) | O(log₃ n) | O(log₃ n) | O(1) |
| `interpolation_search` (via `binary_search`) | O(1) | O(log log n) | O(n) | O(1) |
| `sentinel_linear_search` | O(1) | O(n) | O(n) | O(1) |
| `double_linear_search` | O(1) | O(n) | O(n) | O(1) |
| `quick_select` | O(n) | O(n) | O(n²) | O(1) |
| `median_of_medians` | O(n) | O(n) | O(n) | O(log n) |
| `binary_tree_traversal` | O(n) | O(n) | O(n) | O(h) |
| `hill_climbing` | O(1) | O(iter) | O(iter) | O(1) |
| `simulated_annealing` | O(1) | O(iter) | O(iter) | O(1) |
| `tabu_search` | O(1) | O(iter·n) | O(iter·n) | O(tabu_size) |

---

## Sorts

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| `bubble_sort` | O(n) | O(n²) | O(n²) | O(1) | Yes |
| `insertion_sort` | O(n) | O(n²) | O(n²) | O(1) | Yes |
| `selection_sort` | O(n²) | O(n²) | O(n²) | O(1) | No |
| `merge_sort` | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| `quick_sort` | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| `quick_sort_3_partition` | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| `heap_sort` | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| `counting_sort` | O(n+k) | O(n+k) | O(n+k) | O(k) | Yes |
| `radix_sort` | O(nk) | O(nk) | O(nk) | O(n+k) | Yes |
| `bucket_sort` | O(n+k) | O(n+k) | O(n²) | O(n) | Yes |
| `tim_sort` | O(n) | O(n log n) | O(n log n) | O(n) | Yes |
| `shell_sort` (via `shrink_shell_sort`) | O(n log n) | O(n log²n) | O(n²) | O(1) | No |
| `comb_sort` | O(n log n) | O(n²/2ᵖ) | O(n²) | O(1) | No |
| `cycle_sort` | O(n²) | O(n²) | O(n²) | O(1) | No |
| `cocktail_shaker_sort` | O(n) | O(n²) | O(n²) | O(1) | Yes |
| `gnome_sort` | O(n) | O(n²) | O(n²) | O(1) | Yes |
| `bitonic_sort` | O(n log²n) | O(n log²n) | O(n log²n) | O(log²n) | No |
| `odd_even_sort` | O(n) | O(n²) | O(n²) | O(1) | Yes |
| `odd_even_transposition_parallel` | O(n) | O(n) | O(n) | O(n) | Yes |
| `patience_sort` | O(n log n) | O(n log n) | O(n log n) | O(n) | No |
| `strand_sort` | O(n) | O(n√n) | O(n²) | O(n) | Yes |
| `natural_sort` | O(n) | O(n log n) | O(n log n) | O(n) | Yes |
| `topological_sort` | O(V+E) | O(V+E) | O(V+E) | O(V) | — |
| `tree_sort` | O(n log n) | O(n log n) | O(n²) | O(n) | Yes |
| `intro_sort` | O(n log n) | O(n log n) | O(n log n) | O(log n) | No |
| `msd_radix_sort` | O(nk) | O(nk) | O(nk) | O(n+k) | Yes |
| `binary_insertion_sort` | O(n log n) | O(n²) | O(n²) | O(1) | Yes |
| `bogo_sort` | O(n) | O(n·n!) | ∞ | O(1) | No |
| `stooge_sort` | O(n^2.709) | O(n^2.709) | O(n^2.709) | O(n) | No |
| `slowsort` | O(n^(log n/2)) | — | — | O(n) | Yes |
| `stalin_sort` | O(n) | O(n) | O(n) | O(1) | No* |
| `pigeon_sort` | O(n+k) | O(n+k) | O(n+k) | O(k) | Yes |
| `bead_sort` | O(n) | O(√n·max) | O(n²) | O(n·max) | Yes |
| `dutch_national_flag_sort` | O(n) | O(n) | O(n) | O(1) | No |
| `cyclic_sort` | O(n) | O(n) | O(n²) | O(1) | No |
| `wiggle_sort` | O(n) | O(n) | O(n) | O(1) | No |

*Stalin sort deletes out-of-order elements.

---

## Strings

### Pattern Matching
| Algorithm | Preprocessing | Search | Space |
|-----------|--------------|--------|-------|
| `knuth_morris_pratt` | O(m) | O(n) | O(m) |
| `rabin_karp` | O(m) | O(n) avg | O(1) |
| `naive_string_search` | O(1) | O(n·m) | O(1) |
| `aho_corasick` | O(Σm) | O(n+k) | O(Σm) |
| `boyer_moore_search` | O(m) | O(n/m) best | O(m) |
| `bitap_string_match` | O(m) | O(n·m/w) | O(m) |
| `manacher` | O(n) | — | O(n) |
| `prefix_function` (KMP failure) | O(m) | — | O(m) |

### Edit Distance & Similarity
| Algorithm | Metric | Complexity |
|-----------|--------|------------|
| `levenshtein_distance` | Insert/delete/replace | O(n·m) |
| `damerau_levenshtein_distance` | + transposition | O(n·m) |
| `hamming_distance` | Bit-flip count | O(n) |
| `jaro_winkler` | Jaro + prefix bonus | O(n·m) |
| `min_cost_string_conversion` | Weighted edit | O(n·m) |

### Validation & Detection
| Algorithm | Checks |
|-----------|--------|
| `is_pangram` | All 26 letters present |
| `is_isogram` | No repeated letters |
| `is_contains_unique_chars` | All chars distinct |
| `can_string_be_rearranged_as_palindrome` | Even freq counts |
| `check_anagrams` | Same sorted chars |
| `barcode_validator` | EAN-13 checksum |
| `credit_card_validator` | Luhn algorithm |
| `is_valid_email_address` | RFC-compliant regex |
| `is_indian_phone_number` | +91 format |
| `is_spain_national_id` | DNI validation |

### Formatting & Transformation
| Algorithm | Transform |
|-----------|---------|
| `lower` / `upper` / `capitalize` / `title` | Case conversion |
| `camel_case_to_snake_case` | CamelCase → snake_case |
| `snake_case_to_camel_pascal_case` | snake_case → Camel/Pascal |
| `string_switch_case` | Toggle every character's case |
| `strip` / `split` / `join` | String utilities |
| `pig_latin` | Pig Latin encoding |
| `wave_string` | Alternate upper/lower |
| `text_justification` | Word wrap with alignment |
| `reverse_words` / `reverse_letters` | Reversal variants |
| `remove_duplicate` | Remove repeated chars |
| `ngram` | n-gram tokenization |
| `anagrams` | Generate all anagram groups |

### Advanced
| Algorithm | Use Case |
|-----------|---------|
| `aho_corasick` | Multi-pattern search (e.g., antivirus) |
| `autocomplete_using_trie` | Prefix suggestions |
| `wildcard_pattern_matching` | `?` and `*` glob |
| `word_pattern` | Bijective word↔symbol mapping |
| `word_occurrence` | Word frequency count |
| `top_k_frequent_words` | Heap-based top-k |
| `frequency_finder` | Letter frequency analysis |
| `detecting_english_programmatically` | Language detection |
| `dna` | DNA sequence operations |

---

## Web Programming

HTTP-based scrapers and API clients. Network-dependent — use `# doctest: +SKIP`.

| Script | Source / API |
|--------|-------------|
| `fetch_github_info` | GitHub REST API v3 |
| `fetch_quotes` | Quotes API |
| `nasa_data` | NASA APOD API |
| `get_ip_geolocation` | IP geolocation API |
| `co2_emission` | World Bank CO₂ data |
| `world_covid19_stats` | COVID-19 statistics API |
| `get_top_hn_posts` | Hacker News Firebase API |
| `reddit` | Reddit JSON API |
| `search_books_by_isbn` | Open Library API |
| `currency_converter` | Exchange rate API |
| `current_weather` | OpenWeatherMap API |
| `current_stock_price` | Yahoo Finance scrape |
| `get_amazon_product_data` | Amazon page scrape |
| `get_imdb_top_250_movies_csv` | IMDb scrape |
| `get_top_billionaires` | Forbes scrape |
| `crawl_google_results` | Google SERP scrape |
| `emails_from_url` | Email extraction regex |
| `fetch_bbc_news` | BBC News RSS |
| `fetch_anime_and_play` | AniList / streaming |
| `instagram_crawler` | Instagram public data |
| `giphy` | GIPHY API |
| `daily_horoscope` | Horoscope scrape |
| `slack_message` | Slack Incoming Webhooks |
| `recaptcha_verification` | Google reCAPTCHA v2 |
| `download_images_from_google_query` | Google Images scrape |

---

## Design Philosophy

**Each algorithm ships in two files:**

```python
# merge_sort.py — canonical implementation
def merge_sort(arr: list) -> list:
    """
    Sort a list using merge sort.

    >>> merge_sort([3, 1, 4, 1, 5, 9])
    [1, 1, 3, 4, 5, 9]
    >>> merge_sort([])
    []
    """
    ...

# merge_sort_optimized.py — compare approaches
def benchmark():
    import timeit
    setup = "from __main__ import merge_sort_v1, merge_sort_v2, ..."
    for name, fn in variants:
        t = timeit.timeit(f"{fn}(data[:])", setup=setup, number=1000)
        print(f"{name}: {t:.4f}s")
```

**Every optimized file answers:** *Which implementation wins, and why?*

---

## Running Tests

```bash
# Single algorithm
python -m doctest sorts/merge_sort.py -v

# Entire category
for f in sorts/*.py; do python -m doctest "$f"; done

# Run benchmarks
python -c "from sorts.merge_sort_optimized import benchmark; benchmark()"
```

---

## Dependencies

```
requests==2.33.1          # HTTP client (web_programming)
beautifulsoup4==4.14.3    # HTML parsing (web_programming)
lxml==6.0.4               # Fast XML/HTML parser
numpy==2.4.4              # Numerical arrays (audio, vision, ML)
```

Install: `pip install -r requirements.txt`

---

## Complexity Cheat Sheet

| Operation | Best Algorithm | Complexity |
|-----------|---------------|------------|
| Sort (comparison) | Merge/Heap/Tim | O(n log n) |
| Sort (integer keys) | Radix / Count | O(nk) |
| Search (sorted array) | Binary Search | O(log n) |
| Search (unsorted) | Linear | O(n) |
| String match (single) | KMP / Boyer-Moore | O(n+m) |
| String match (multi) | Aho-Corasick | O(n+Σm+k) |
| Shortest path | Dijkstra | O((V+E)log V) |
| All-pairs shortest | Floyd-Warshall | O(V³) |
| Min spanning tree | Kruskal / Prim | O(E log V) |
| Max flow | Dinic's | O(V²E) |
| Union-Find | Path compress + rank | O(α(n)) ≈ O(1) |
| LCS / Edit distance | DP table | O(n·m) |
| Convex hull | Graham Scan | O(n log n) |
| Matrix multiply | Strassen | O(n^2.807) |
| Primality test | Miller-Rabin | O(k log²n log log n) |
| Integer factorize | Pollard's ρ | O(n^(1/4)) |
| Hash (cryptographic) | SHA-256 | O(n) |

---

## License

MIT — free to use, study, and adapt. Attribution appreciated.

---

*Source implementations adapted from [TheAlgorithms/Python](https://github.com/TheAlgorithms/Python), enhanced with optimized variants, benchmarks, and interview-focused annotations.*
