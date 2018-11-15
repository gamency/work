
/**
 * 在这里给出对类 Part4 的描述。
 * 
 * @作者（你的名字）
 * @版本（一个版本号或者一个日期）
 */

import edu.duke.*;

public class Part4 {
public void readUrl(Iterable<String> words){
    //String link = "http://www.dukelearntoprogram.com/course2/data/manylinks.html";
    //URLResource res = new URLResource(link);
    for (String word : words) {
        //System.out.println(word);
        int youtubeIndex = word.toLowerCase().indexOf("youtube.com");
        System.out.println(youtubeIndex);
        if (youtubeIndex != -1){
            int rightquoteIndex = word.indexOf("\"");
            int leftquoteIndex = word.indexOf("\"", rightquoteIndex + 1);
            System.out.println("****" + rightquoteIndex + leftquoteIndex);
            String linkurl = word.substring(rightquoteIndex + 1, leftquoteIndex);
            //int youtubeIndex = linkurl.indexOf("youtube.com");
            System.out.println(linkurl);
        }
        System.out.println("--------");
    }
}
public static Iterable<String> readURL(String url){
    URLResource ur = new URLResource(url);
    return ur.words();
}
public void test(){
    //String link = "http://www.dukelearntoprogram.com/course2/data/manylinks.html";
    Iterable<String> words = readURL("http://www.dukelearntoprogram.com/course2/data/manylinks.htm");
    readUrl(words);
}

public static void main(String [] args) {
    Part4 pt = new Part4();
    pt.test();
}
}
