
/**
 * 在这里给出对类 Part3 的描述。
 * 
 * @作者（你的名字）
 * @版本（一个版本号或者一个日期）
 */
public class Part3 {
    public boolean twoOccurrences (String stringa, String stringb){
        int index = stringb.indexOf(stringa);
        int flag = 1;
        int occurNum = 0;
        while (flag == 1){
            if ( index == -1){
                flag = -1;
                //return false;
            }
            else {
                occurNum += 1;
            }
            index = stringb.indexOf(stringa, index + 1);
        }
        if (occurNum < 2){
            return false;
        }
        else {
            return true;
        }
    }
    
    public String lastPart(String stringa, String stringb){
        int index = stringb.indexOf(stringa);
        if (index == -1){
            return stringb;
        }
        else
        {
            return stringb.substring(index + stringa.length());
        }
    }
    
    public void testing(){
        String stringa = "zoo";
        String stringb = "forest-zoo-adsfk-zoo";
        
        System.out.println(twoOccurrences("by", "A story by Abby Long"));
        System.out.println(twoOccurrences("a", "banana"));
        System.out.println(twoOccurrences("atg", "ctgtatgta"));
        
        System.out.println(twoOccurrences("an", "banana"));
        System.out.println(twoOccurrences("zoo", "forest"));
        System.out.println(twoOccurrences("zoo", "farzookeeper"));
        
        System.out.println("The stringa is: " + stringa + " The stringb is: " + stringb + " match is: " + twoOccurrences(stringa, stringb));
        
        System.out.println(lastPart("an", "banana"));
        System.out.println(lastPart("zoo", "forest"));
        System.out.println(lastPart("zoo", "farzookeeper"));
        System.out.println("The stringa is: " + stringa + " The stringb is: " + stringb + " match is: " + lastPart(stringa, stringb));
    }
    
    public static void main(String [] args){
        Part3 pr = new Part3();
        pr.testing();
    }
}
