
/**
 * Illustrate Character methods
 * 
 * @author Duke Software Team 
 * @version (a version number or a date)
 */
public class CharacterDemo {
    public void digitTest() {
        String test = "ABCabc0123456789';#!";
        for(int k=0; k < test.length(); k++){
            char ch = test.charAt(k);
            if (Character.isDigit(ch)){
               System.out.println(ch+" is a digit"); 
            }
            if (Character.isAlphabetic(ch)){
                System.out.println(ch+" is alphabetic");
            }
            if (ch == '#'){
                System.out.println(ch +" #hashtag");
            }
        }
    }
    
    public boolean isVowels(char ch) {
        String test = "AEIOUaeiou";
        
        if ( test.indexOf(ch) != -1){
            return true;
        }
        
        return false;
    }
    
    public String replaceVowels(String phrase, char ch){
        StringBuilder s = new StringBuilder(phrase);
        for (int i = 0; i < phrase.length(); i++){
            char chi = phrase.charAt(i);
            if ( isVowels(chi)  ){
                s.setCharAt(i, ch);
            }
        }
        return s.toString();
    }
    
    public String emphasize(String phrase, char ch){
        StringBuilder s = new StringBuilder(phrase);
        char start = '*';
        char addSign = '+';
        for (int i = 0; i < phrase.length(); i++){
            if ( phrase.charAt(i) == ch){
                if ( i % 2 == 0){
                    s.setCharAt(i, start);
                }
                else{
                    s.setCharAt(i, addSign);
                }
            }
            
        }
        return s.toString();
    }
    

    
    public void conversionTest(){
        String test = "ABCDEFabcdef123!#";
        for(int k=0; k < test.length(); k++){
            char ch = test.charAt(k);
            char uch = Character.toUpperCase(ch);
            char lch = Character.toLowerCase(ch);
            System.out.println(ch+" "+uch+" "+lch);
        }
    }
}
