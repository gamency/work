
/**
 * 在这里给出对类 Part1 的描述。
 * 
 * @作者（你的名字）
 * @版本（一个版本号或者一个日期）
 */
public class Part1 {
    public String findSimpleGene (String dna){
        String tmp = "";
        int start = dna.indexOf("atg");
        if (start == -1){
            return tmp;
        }
        
        int stop = dna.indexOf("taa", start + 3);
        if (stop == -1){
            return tmp;
        }
        if ((stop - start) % 3 == 0) {
            return dna.substring(start, stop + 3);
        }
        else {
            return tmp;
        }
    }
    
    public void testSimpleGene(){
        String a = "cccatggggtttaaataataataggagagagagagagagttt";
        String ap = "atggggtttaaataataatag";
        String result = findSimpleGene(ap);
        System.out.println("dna string is " + ap);
        System.out.println("gene is" + result);
    }
    public static void main (String[] args){
        Part1 gene = new Part1();
        gene.testSimpleGene();
    }
}
