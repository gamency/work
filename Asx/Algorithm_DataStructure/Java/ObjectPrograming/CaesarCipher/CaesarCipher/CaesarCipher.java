import edu.duke.*;

public class CaesarCipher {
    public String encrypt(String input, int key) {
        //Make a StringBuilder with message (encrypted)
        StringBuilder encrypted = new StringBuilder(input);
        //Write down the alphabet
        String alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        String alphabetlower = "abcdefghijklmnopqrstuvwxyz";
        //Compute the shifted alphabet
        String shiftedAlphabet = alphabet.substring(key)+
        alphabet.substring(0,key);
        
        String shiftedAlphabetlower = alphabetlower.substring(key)+
        alphabetlower.substring(0,key);
        //Count from 0 to < length of encrypted, (call it i)
        for(int i = 0; i < encrypted.length(); i++) {
            //Look at the ith character of encrypted (call it currChar)
            char currChar = encrypted.charAt(i);
            //Find the index of currChar in the alphabet (call it idx)
            //int idx = alphabet.indexOf(currChar);
            
            if (shiftedAlphabet.indexOf(currChar) != -1){
                int idx = alphabet.indexOf(currChar);
                char newChar = shiftedAlphabet.charAt(idx);
                encrypted.setCharAt(i, newChar);
            }
            
            if (shiftedAlphabetlower.indexOf(currChar) != -1){
                int idx = alphabetlower.indexOf(currChar);
                char newChar = shiftedAlphabetlower.charAt(idx);
                encrypted.setCharAt(i, newChar);
            }
            //If currChar is in the alphabet
            //if(idx != -1){
                //Get the idxth character of shiftedAlphabet (newChar)
            //    char newChar = shiftedAlphabet.charAt(idx);
                //Replace the ith character of encrypted with newChar
            //    encrypted.setCharAt(i, newChar);
            //}
            //Otherwise: do nothing
        }
        //Your answer is the String inside of encrypted
        return encrypted.toString();
    }
    
    public char encryptChar(char input, int key) {
		String alphabet = "abcdefghijklmnopqrstuvwxyz";

		if(Character.isUpperCase(input)) {
			String shifted = alphabet.toUpperCase().substring(key);
			shifted += alphabet.toUpperCase().substring(0, key);

			int currIndex = alphabet.toUpperCase().indexOf(input);
			char encrypted = shifted.charAt(currIndex);
			return encrypted;
		}

		if(Character.isLowerCase(input)) {
			String shifted = alphabet.toLowerCase().substring(key);
			shifted += alphabet.toLowerCase().substring(0, key);

			int currIndex = alphabet.toLowerCase().indexOf(input);
			char encrypted = shifted.charAt(currIndex);
			return encrypted;	
		}

		return '\0';
	}

	/*
	 * This method returns a String that has been encrypted using the following algorithm. 
	 * Parameter key1 is used to encrypt every other character with the Caesar Cipher 
	 * algorithm, starting with the first character, and key2 is used to encrypt every 
	 * other character, starting with the second character
	 */
	public String encryptTwoKeys(String input, int key1, int key2) {
		StringBuilder encrypted = new StringBuilder(input);
		for(int i = 0, n = input.length(); i < n; i++) {
			char currChar = input.charAt(i);
			if((i + 1) % 2 == 0) {	// If the character is even
				char encrChar = encryptChar(currChar, key2);
				encrypted.setCharAt(i, encrChar);
			}

			if((i + 1) % 2 != 0) {	// If the character is odd
				char encrChar = encryptChar(currChar, key1);
				encrypted.setCharAt(i, encrChar);	
			}
		}
		return encrypted.toString();
	}
    
    public void testCaesar() {
        int key = 15;
        FileResource fr = new FileResource();
        //String message = fr.asString();
        String message = "At noon be in the conference room with your hat on for a surprise party. YELL LOUD!";
        String encrypted = encrypt(message, key);
        System.out.println(encrypted);
        String decrypted = encrypt(encrypted, 26-key);
        //System.out.println(decrypted);
        String twoKey = encryptTwoKeys(message, 8, 21);
        System.out.println(twoKey);
    }
}

