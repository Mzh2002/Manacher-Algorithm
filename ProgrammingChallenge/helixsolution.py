import sys
import os
import time

#
#Central Idea: a palindrome with 1 mismatch should be the same size or larger as the longest palindromic substring with 0 mismatches 
# if a palindrome with 1 mismatch is equal to the longest palindromic substring with 0 mismatches, that means that palindrome HAS NOT USED THE MISMATCH YET
#so we first used manacher's algo to find the longest palindromic substring with 0 mismatches(LPS0); and then we try to find the longest palindromic substring with 1 mismatch(LPS1) via using manacher's algo again
# At any index of the saved radius lists in LPS1, the value should be at least the same as the value in LPS0; if it is the same value, that means we have not used the mismatch yet; 
# So at index i, if we find the mirrored position of the current index in LPS1 and see that the value saved for the mirroed position is equal to the value stored for LPS0 at index i, we can decude that we have not used the mismatch yet; so we can expand the palindrome outwards until we find a mismatch or hit the edge of the string; and once we do, we use the mismatch and continue expanding until another mismatch or edge is found and stop there. 
# if we find that the value saved for the mirrored position is greater than the value stored for LPS0 at index i, we can deduce that we have used the mismatch already; so we can expand the palindrome outwards until we find a mismatch or edge and stop there. 
# altering manacher's algorithm like this allows us to find the longest palindromic substring with at most 1 mismatch in O(n) (where n is the length of the string) time complexity as saving past values of the radius allows us to not have to recheck the same values over and over again. Space complexity is also O(n) as the largest space we're using is for the radius lists which store the same amount of values as the string length.


#helps us check if two characters are matching pairs A-t C-G and #-# and vice versa
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
    radius0 = [0] * len(s) # radius0 stores the length of the longest palindromic substring with center at i
    radius1 = [0] * len(s) # radius1 stores the length of the longest palindromic substring with one mistake with center at i
    #center0 and right0 correspond to to the center and right edge of the right most palindrome processed so far with 0 mismatches, while center1 and right1 correspond to the same thing but for 1 mismatch
    center0, center1 = 0, 0 
    right0, right1 = 0, 0

    for i in range(1, len(s) - 1):
        #first handle 0 mismatches
        mirrored_pos = 2 * center0 - i #calculate the mirrored position of i with respect to center0

        #checks the value of the mirrored position, we can only use the value if its less than the right edge of the palindrome, otherwise we can only determine that the radius is atmost the distance to the right edge of the palindrome
        if i < right0:
            radius0[i] = min(right0 - i, radius0[mirrored_pos])

        #expand the palindrome out until it either hits the edge of the string or a mismatch is found
        while i + radius0[i] + 1 < len(s) and i - (radius0[i] + 1) >= 0 and matches(s[i + radius0[i] + 1], s[i - (radius0[i] + 1)]):
            radius0[i] += 1
        #update center0 and right 0
        if i + radius0[i] > right0:
            center0 = i
            right0 = i + radius0[i]

        #then do 1 mismatch w manachers
        mirrored_pos1 = 2 * center1 - i

        if i < right1:
            radius1[i] = min(right1 - i, radius1[mirrored_pos1])
        # inherit any perfect‐match radius => if radius[i] is smaller than radius0[i], all that tells us is that radius[i] or the mirrored version isn't fully calculated yet, since we know that radius1[i] should be atleast  as large as radius0[i], we don't need to relook at any radiuses less than radius0[i]
        radius1[i] = max(radius1[i], radius0[i])
        # if no mismatch used yet at this center, try to spend one
        if radius1[i] == radius0[i]:  # No mismatch used yet
            mismatch_used = False
            # Try to expand one position to potentially use our mismatch
            if (i + radius1[i] + 1 < len(s) and 
                i - (radius1[i] + 1) >= 0):
                
                if not matches(s[i + radius1[i] + 1], s[i - (radius1[i] + 1)]):
                    # Found a mismatch, use it
                    radius1[i] += 1
                    mismatch_used = True
            
            # Continue expanding with perfect matches (after possibly using the mismatch)
            while (i + radius1[i] + 1 < len(s) and 
                i - (radius1[i] + 1) >= 0 and 
                matches(s[i + radius1[i] + 1], s[i - (radius1[i] + 1)])):
                radius1[i] += 1
        else:
        #resume perfect matches after the (optional) mismatch
            while i + radius1[i] + 1 < len(s) and i - (radius1[i] + 1) >= 0 and matches(s[i + radius1[i] + 1], s[i - (radius1[i] + 1)]):
                radius1[i] += 1
        #update center1 and right1
        if i + radius1[i] > right1:
            center1 = i
            right1 = i + radius1[i]
    radius = 0
    largestCenter = 0
    #find largest palindrome with 1 mismatch
    for i in range(0, len(s)):
        if radius1[i] > radius:
            radius = radius1[i]
            largestCenter = i
    return postprocess(s[largestCenter - radius:largestCenter + radius + 1])


# start_time = time.perf_counter()
input = sys.stdin.read().strip()
output = helix(input)
# end_time = time.perf_counter()
# time_spent = end_time - start_time
# print(f"Time spent: {time_spent:.6f} seconds")
print(output)
