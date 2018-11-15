
/**
 * 在这里给出对类 Part2 的描述。
 * 
 * @作者（你的名字）
 * @版本（一个版本号或者一个日期）
 */
public class Part2 {
    
    public int howMany(String stringa, String stringb){
        int index = stringb.indexOf(stringa);
        int occurrenceNum = 0;
        while (index != -1){
            occurrenceNum += 1;
            index = stringb.indexOf(stringa, index + stringa.length());
        }
        return occurrenceNum;
    }
    
    public void testHowMany(){
        String a = "AA";
        String b = "ATAAAAA";
        int occurrenceNum = howMany(a,b);
        System.out.println(occurrenceNum);
    }
}
