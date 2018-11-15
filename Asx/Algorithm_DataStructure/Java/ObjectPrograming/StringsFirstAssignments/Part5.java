
/**
 * 在这里给出对类 Part5 的描述。
 * 
 * @作者（你的名字）
 * @版本（一个版本号或者一个日期）
 */

import edu.duke.URLResource;
public class Part5 {
public static void main(String[] args) {


        Iterable<String> words = readURL("http://www.dukelearntoprogram.com/course2/data/manylinks.html");

        findLink(words);


    }

    public static Iterable<String> readURL(String url) {

        URLResource ur = new URLResource(url);

        return ur.words();

    }

    public static void findLink(Iterable<String> words) {

        String searchWord = "youtube.com";

        for (String s : words) {
            int pos = s.toLowerCase().indexOf(searchWord);

            if (pos != -1) {

                int beg = s.lastIndexOf("\"", pos);
                int end = s.indexOf("\"", pos + 1);
                String w = s.substring(beg + 1, end);

                System.out.format("Start: %s, End: %s \n", beg, end);
                System.out.println(w);

            }
        }

    }
}
