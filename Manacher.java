public class Manacher {
    /**
     * Manacher's algorithm exploits the idea that there are mirrored palindromes are within a larger palindrome.
     *
     * We have three cases:
     *
     * Case 1. If the palindrome at the current center falls completely within the right and left boundaries
     * when calculated with the mirrored index, we have found the palindrome for that particular point.
     *
     * Case 2. If the palindrome at the current center reaches exactly to the right boundary
     * when calculated with the mirrored index, we have to manually expand the palindrome beyond the right boundary.
     *
     * Case 3. If the palindrome at the current center falls outside the right boundary
     * when calculated with the mirrored index, we have to reduce the radius to fit within the right boundary.
     * After that, manually expand the palindrome.
     *
     * Any time we have the current index past the right boundary, we manually expand a palindrome.
     */
    public static String manacher(String s) {
        // Preprocess the string with '#' in between characters to find even-length palindromes
        StringBuilder sb = new StringBuilder("#");
        for (char c : s.toCharArray()) {
            sb.append(c).append("#");
        }
        String t = sb.toString();

        int n = t.length();

        // Array to store palindrome radii
        int[] p = new int[n];

        // Center of old rightmost palindrome
        int center = 0;

        // Right boundary of the rightmost palindrome
        int right = 0;

        // Length of the longest palindrome found so far
        int maxLen = 0;

        // Center index of the longest palindrome found
        int centerIndex = 0;

        // Iterate through all indices
        for (int i = 1; i < n - 1; i++) {
            // Find the mirrored index reflected across old center
            int mirror = 2 * center - i;

            // Case 1 and 3
            if (i < right) {
                p[i] = Math.min(right - i, p[mirror]);
            }

            // Case 2 and 3
            while (i + (1 + p[i]) < n && i - (1 + p[i]) >= 0 && t.charAt(i + (1 + p[i])) == t.charAt(i - (1 + p[i]))) {
                p[i]++;
            }

            // In case 2 and 3, if we expand beyond the right boundary, update old center and right
            if (i + p[i] > right) {
                center = i;
                right = i + p[i];
            }

            // Track the longest palindrome
            if (p[i] > maxLen) {
                maxLen = p[i];
                centerIndex = i;
            }
        }

        // Extract the longest palindrome from the original string
        int start = (centerIndex - maxLen) / 2;
        return s.substring(start, start + maxLen);
    }

    public static void testManacher() {
        String s1 = "abcba";
        System.out.println("Test Case 1: " + manacher(s1));

        String s2 = "abaxyzzyxf";
        System.out.println("Test Case 2: " + manacher(s2));

        String s3 = "xyzracecarabc";
        System.out.println("Test Case 3: " + manacher(s3));

        String s4 = "fgjijkllkjljgf";
        System.out.println("Test Case 4: " + manacher(s4));

        String s5 = "abacdfgdcabbaabcdedcba";
        System.out.println("Test Case 5: " + manacher(s5));
    }

    public static void main(String[] args) {
        testManacher();
    }
}
