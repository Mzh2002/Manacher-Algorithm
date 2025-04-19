
import random
import time
import os
from pathlib import Path

def brute_max_valid_helix(s: str) -> str:
    comp = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}
    n = len(s)
    best = ""
    for i in range(n):
        for j in range(i+1, n+1):
            sub = s[i:j]
            l, r = 0, len(sub) - 1
            mismatches = 0
            while l < r:
                if comp.get(sub[l]) != sub[r]:
                    mismatches += 1
                    if mismatches > 1:
                        break
                l += 1
                r -= 1
            else:
                if len(sub) > len(best):
                    best = sub
    return best
def delete_files_with_test_in_name(directory='.'):
    """
    Delete all files in the given directory (and its subdirectories) whose
    filename contains the substring 'test' (case-insensitive).
    """
    for path in Path(directory).rglob('*'):
        if path.is_file() and 'test' in path.name.lower() or "expected" in path.name.lower():
            path.unlink()
            print(f"Deleted file by name: {path}")
    time.sleep(1)  # Sleep for 1 second to ensure file deletion is complete

def generate_test_case(size_range) -> str:
    n = random.randint(size_range[0], size_range[1])
    s = ''.join(random.choice('ATCG') for _ in range(n))
    return s
matching_pairs = {
    'A': 'T',
    'T': 'A',
    'C': 'G',
    'G': 'C',
    '#': '#',
}
#adds a # to the beginning and end of the string and adds a # between each character in the string
#this is done to make the string odd length and to make it easier to check for palindromes
def preprocess(s):
    s = "#" + "#".join(s) + "#" 
    return s
#removes all the # from the string and returns it
def postprocess(s):
    s = s.replace("#", "")
    return s
#compares if two characters are matching pairs
def matches(a, b):
    if matching_pairs[a] == b:
        return True
    return False
def helix(s):
    s = preprocess(s)
    radius0 = [0] * len(s) # p0 stores the length of the longest palindromic substring with center at i
    radius1 = [0] * len(s) # p1 stores the length of the longest palindromic substring with one mistake with center at i+1
    #center0 and right0 correspond to to the center and right edge of the right most palindrome processed so far with 0 mismatches, while center1 and right1 correspond to the same thing but for 1 mismatch
    center0, center1 = 0, 0 
    right0, right1 = 0, 0
    #Central Idea: a palindrome with 1 mismatch should be the same size or larger as the longest palindromic substring with 0 mismatches 
    # if a palindrome with 1 mismatch is equal to the longest palindromic substring with 0 mismatches, that means that palindrome HAS NOT USED THE MISMATCH YET
    #so we first used manacher's algo to find the longest palindromic substring with 0 mismatches(LPS0); and then we try to find the longest palindromic substring with 1 mismatch(LPS1) via using manacher's algo again
    # At any index of the saved radius lists in LPS1, the value should be at least the same as the value in LPS0; if it is the same value, that means we have not used the mismatch yet; 
    # So at index i, if we find the mirrored position of the current index in LPS1 and see that the value saved for the mirroed position is equal to the value stored for LPS0 at index i, we can decude that we have not used the mismatch yet; so we can expand the palindrome outwards until we find a mismatch or hit the edge of the string; and once we do, we use the mismatch and continue expanding until another mismatch or edge is found and stop there. 
    # if we find that the value saved for the mirrored position is greater than the value stored for LPS0 at index i, we can deduce that we have used the mismatch already; so we can expand the palindrome outwards until we find a mismatch or edge and stop there. 



    for i in range(1, len(s) - 1):
        #first handle 0 mismatches
        mirrored_pos = 2 * center0 - i #calculate the mirroed position of i with respect to center0

        #checks the value of the mirrored position, we can only use the value if its less than the right edge of the palindrome, otherwise we can only determine that the radius is atmost the distance to the right edge of the palindrome
        if i < right0:
            radius0[i] = min(right0 - i, radius0[mirrored_pos])

        #expand the palindrome out until it either hits the edge of the string or a mismatch is found
        while i + radius0[i] + 1 < len(s) and i - (radius0[i] + 1) >= 0 and matches(s[i + radius0[i] + 1], s[i - (radius0[i] + 1)]):
            radius0[i] += 1


        #then do 1 mismatch...
        mirrored_pos1 = 2 * center1 - i
        #check if the mirrored position is less than the right edge of the palindrome, if it is, we can use the value stored at the mirrored position; otherwise we can only determine that the radius is atmost the distance to the right edge of the palindrome
        if i < right1:
            radius1[i] = min(right1 - i, radius1[mirrored_pos1])
        #if radius[i] is smaller than radius0[i], all that tells us is that radius[i] or the mirrored version isn't fully calculated yet, since we know that radius1[i] should be atleast  as large as radius0[i], we don't need to relook at any radiuses less than radius0[i]
        radius1[i] = max(radius1[i], radius0[i])
            
        if radius1[i] == radius0[i]:
            #this means a mismatch hasn't been used yet; we can use the first mismatch in the longest palindromic substring with one mistake with center at i+1
            while i + radius1[i] + 1 < len(s) and i - (radius1[i] + 1) >= 0:
                radius1[i] += 1
                if matches(s[i + radius1[i]], s[i - (radius1[i])]) == False:
                    break
                
        #mismatch should be used at at his point if there was one; expand until we hit another mismatch or the edge of the string
        while i + radius1[i] + 1 < len(s) and i - (radius1[i] + 1) >= 0 and matches(s[i + radius1[i] + 1], s[i - (radius1[i] + 1)]):
            radius1[i] += 1
        if i + radius1[i] > right1:
            center1 = i
            right1 = i + radius1[i]
    radius = 0
    largestCenter = 0
    #find largest value
    for i in range(0, len(s)):
        if radius1[i] > radius:
            radius = radius1[i]
            largestCenter = i
    return postprocess(s[largestCenter - radius:largestCenter + radius + 1])
delete_files_with_test_in_name()
small_test_case_range = (1, 100)
medium_test_case_range = (100, 10000)
large_test_case_range = (10000, 20000)
larger = (20000, 50000)
largest = (1000000, 1000001)

test_cases = [
    (""),
    ("A"),
    ("AT"),
    ("AG"),
    ("AAA"),
    ("CAGC"),
    ("GTACCGTT"),
    ("ACGT"),
    ("ACGTAC"),
    ("ATATAT"),
]
for i in range(21):
    #generate test case 
    res = ""
    if i <= 9:
        res = test_cases[i]
    elif i <= 12:
        res = generate_test_case(small_test_case_range)
    elif i <= 15:
        res = generate_test_case(medium_test_case_range)
    elif i <= 18:
        res = generate_test_case(large_test_case_range)
    elif i <= 20:
        res = generate_test_case(larger)
    else:
        res = generate_test_case(largest)
    with open(f"test.in.{i}", "w") as infile:
        infile.write(res + "\n")
    # generate expected output
    #calculate time spent

    start_time = time.perf_counter()

    expected_output = brute_max_valid_helix(res)
    end_time = time.perf_counter()
    time_spent = end_time - start_time
    with open(f"test.out.{i}", "w") as outfile:
        outfile.write(expected_output + "\n")

    print(f"Test case {i} generated with size {len(res)} and expected output {expected_output} and spent {time_spent:.4f} seconds")
i = 21
res = generate_test_case(largest)
with open(f"test.in.{i}", "w") as infile:
    infile.write(res + "\n")
# # generate expected output
# calculate time spent
start_time = time.perf_counter()
expected_output = helix(res)
end_time = time.perf_counter()
time_spent = end_time - start_time
with open(f"test.out.{i}", "w") as outfile:
    outfile.write(expected_output + "\n")
print(f"Test case {i} generated with size {len(res)} and expected output {expected_output} and spent {time_spent:.4f} seconds")
print("All test cases generated successfully.")
