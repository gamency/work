
/**
 * 在这里给出对类 de 的描述。
 * 
 * @作者（你的名字）
 * @版本（一个版本号或者一个日期）
 */
public class de {
    public void findAbc(String input) {
        int index = input.indexOf("abc");
        while (true) {
            if (index == -1 || index >= input.length() - 3) {
                break;
            }
            System.out.println(index);
            System.out.println("index " + index);
            //code
            //index -= 1;
           
            String found = input.substring(index+1, index+4);
            System.out.println(found);
            index = input.indexOf("abc", index+4);
            System.out.println("index after updating " + index);
        }
    }
    public void test() {
    //no code yet
     System.out.println("****&*&");
     findAbc("abcdkfjsksioehgjfhsdjfhksdfhuwabcabcajfieowj");
     System.out.println("*&*&");
     findAbc("ttabcesoeiabco");
     System.out.println("*&*&");
     findAbc("abcbabccabcd");
     System.out.println("*&*&");
     findAbc("qwertyabcuioabcp");
     System.out.println("*&*&");
     findAbc("abcabcabcabca");
    }
}
