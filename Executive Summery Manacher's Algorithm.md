# Introduction / Problem Statement

## What's the problem?

If you've spent time programming, you've likely encountered the concept of **palindromes**—sequences that read the same forward and backward. While palindromes might seem like a trivial concept at first, they actually have meaningful applications in fields like **bioinformatics**, **natural language processing (NLP)**, and **data compression**. Here are a few examples:

- **DNA/RNA Structures**: In molecular biology, palindromic regions in DNA and RNA can fold into hairpin or stem-loop structures, which play key roles in gene regulation and function.
- **Pattern Recognition**: In data compression, algorithms like **LZ77** and **LZ78** can exploit palindromic patterns to identify and compress repeated structures more effectively.
- **Error Correction**: Some advanced encoding schemes use palindromic properties to enhance data integrity and support robust error detection.

From an algorithmic standpoint, checking whether a string is a palindrome is relatively simple—it’s often one of the first challenges beginners tackle. However, problems that involve **finding** or **constructing** palindromes are far more complex. Palindromes are fascinating to algorithm enthusiasts because of their inherent **symmetry**, which challenges the more linear way humans typically think about problems.

Today’s problem is one of the most classic and elegant: 

> Find the **longest palindromic substring** in a given string (A *substring* refers to a contiguous sequence of characters within a string).

## Some Naive Approaches

To find the longest palindromic substring in a given string, the most naive approach uses two nested loops to generate all possible substrings and check each one:

```python
for start in range(len(s)):
	for end in range(start + 1, len(s)):
  	check_is_palindrome(s[start:end+1])
```

This method has a time complexity of **O(n³)**: one layer for the start index, one for the end index, and another for checking if the substring itself is a palindrome (which takes O(n) time). Clearly, this is inefficient and impractical for long strings (Like DNA/RNA sequences or massive data compression).

If we look more closely at the structure of palindromes, we realize that using `start` and `end` to define substrings is not optimal. Palindromes are **symmetric**, so instead of scanning all possible substrings, we can iterate through each character and expand outward from it as a **center**:

```python
for i in range(len(s)):
  radius = 0
  while i - radius >= 0 and i + radius < len(s) and s[i - radius] == s[i + radius]:
    radius += 1
  max_length = 2 * radius + 1
```

* This approach is more intuitive and avoids checking every substring, but it still has two major drawbacks:
  - **Time complexity is still O(n²)**: In the worst case, each center may expand up to the entire string.
  - **It only detects odd-length palindromes**: since the center is assumed to be a single character. Even-length palindromes (like `"abba"`) are ignored.

## Our Goal

To overcome these limitations, the algorithm we seek should:

>* **Achieve a target runtime of O(n).**
>* **Be able to detect both even- and odd-length palindromes efficiently in any string.**

# Manacher's Algorithm - Idea

## Detect both even- and odd-length palindromes

Let’s start solving the problem! 

Before we dive into optimizing performance, we’ll first address a foundational challenge: **how to uniformly detect both odd- and even-length palindromes**. 

Odd-length palindromes are naturally handled when we expand around a single character. The real difficulty lies in **even-length palindromes**. Intuitively, we can interpret these palindromes to have a center between characters. For example:

```
ab ba
  ^
 use this as the center
```

How can we formalize this idea?

We can treat the *space* between every pair of characters as a valid center by **inserting a special character** between each letter. This character should not interfere with the original string’s content—so instead of inserting an actual letter (which could create false matches), we typically use a **non-alphabetic symbol like `#`**. For example:

```
abba => #a#b#b#a#
abcdef => #a#b#c#d#e#f#
```

After this transformation, we no longer need to distinguish between even- and odd-length palindromes—**every palindrome is now centered on a single character**, whether it’s a letter or a `#`.

* **Odd-length palindromes** now center on actual characters:

  ```
  #a#b#c#b#a#
       ^
    normal character 'c' is the center
  ```

* **Even-length palindromes** now center on the `#` characters:

  ```
  #a#b#b#a#
      ^
    '#' is the center
  ```

## Achieve O(n) runtime

Now comes the real challenge: **how do we achieve O(n) runtime?**

Let’s revisit our earlier algorithm:

```python
for i in range(len(s)):
  radius = 0
  while i - radius >= 0 and i + radius < len(s) and s[i - radius] == s[i + radius]:
    radius += 1
  max_length = 2 * radius + 1
```

The good news is that we already have a single outer loop, iterating through all possible centers. So, if we can reduce the **inner palindrome expansion** to **amortized O(1)** per center, the entire algorithm will run in **O(n)** time.

This is where we borrow an idea similar to **dynamic programming**: instead of recomputing everything from scratch, we **store useful information** from earlier computations and reuse it when possible.

What kind of information can we store? Let’s examine an example:

```
#a#b#c#b#c#b#a#
     ^ ~ ^
```

What can we say about the length of the longest palindromic substring centered at two characters marked by `^`? They are the same! How do we know? Except for just counting them, we can also tell this by the fact that they are at two **symmetrical positions** with respect to the center `~` (which is `b` in the middle). If we already know that the entire region around `~` forms a palindrome, then:

- The substring centered at the left `^` has a known radius.
- The substring centered at the right `^` must have **at least the same radius** unless it hits the boundary of the longer palindrome.

This observation leads to a key optimization:

> **If a center lies within a previously known palindrome, its mirrored counterpart (with respect to the current center of the known palindrome) has already computed useful information.**

Therefore, instead of expanding every center from scratch, we can:

- Maintain the **rightmost boundary** of any palindrome found so far and its **corresponding center**.
- Keep an array `P` to store the radius of the longest palindromic substring centered on each character.
- Use the **mirror** of the current character about the stored center to guess the radius (stored in `P`).
- Only expand further if the guessed radius reaches the boundary.

This is the core insight behind **Manacher’s Algorithm**, which leverages symmetry and previously computed results to eliminate redundant computations and bring the runtime down to **O(n)**.

# Manacher's Algorithm - Implementation



Now let's dig into detailed implementation. First, insert `#` into the string:

```python
new_s = '#' + "#".join(s) + '#'
```

We need to keep track of the following three values:

```python
p = [0] * n  # p[i] will hold the radius of the longest palindrome centered at i
center = 0   # The center of the palindrome that extends farthest to the right (i.e. rightmost palindrome)
right = 0    # The right boundary of the palindrome centered at 'center'
```

Next, we begin scanning the string to find the longest palindromic substring centered at each character. Before expanding from a center to check for palindromes, we first try to **leverage previously computed information**. Since we’ve already recorded palindromic spans up to "`right`", we can use this information to make an **initial guess** about the radius at the current center. 

```python
for i in range(n):
	mirror = 2 * center - i  # Mirror position of i around the current center

  if i < right:
    # Use the mirror's result if it doesn't go beyond the right boundary
    # Length of the new palindrome should be at least the same as its mirror
    p[i] = min(right - i, p[mirror])
```

Next, we attempt to **expand beyond the guessed radius** to find the actual longest palindrome centered at the current position—just like in the traditional center-expansion approach. 

If this newly found palindrome extends past the current `right` boundary, we update both `center` and `right` to reflect the new rightmost-reaching palindrome.

```python
for i in range(n):
        mirror = 2 * center - i 

        if i < right:
            p[i] = min(right - i, p[mirror])

        # Attempt to expand the palindrome centered at i beyond guessed raduis
        # Compare characters symmetrically around i as long as they match
        while i + p[i] + 1 < n and i - p[i] - 1 >= 0 and t[i + p[i] + 1] == t[i - p[i] - 1]:
            p[i] += 1

        # If the expanded palindrome goes beyond the current right boundary,
        # update the center and right to reflect the new rightmost palindrome
        if i + p[i] > right:
            center = i
            right = i + p[i]
```



