
/**
 * 在这里给出对类 Part3 的描述。
 * 
 * @作者（你的名字）
 * @版本（一个版本号或者一个日期）
 */

//import Part1.*;
public class Part3 {
    public int findStopCodon(String dna, int startIndex, String stopCodon){
        int currIndex = dna.indexOf(stopCodon, startIndex + 3);
        
        while( currIndex != -1){
            if ((currIndex - startIndex) % 3 == 0){
                return currIndex + 3;
            }
            else{
                currIndex = dna.indexOf(stopCodon, currIndex + 1);
            }
        }
        
        return dna.length();
    }
    
    public String findGene(String dna){
        int startIndex = dna.indexOf("ATG");
        
        if (startIndex == -1){
            return "";
        }
        int taaIndex = findStopCodon(dna, startIndex, "TAA");
        int tagIndex = findStopCodon(dna, startIndex, "TAG");
        int tgaIndex = findStopCodon(dna, startIndex, "TGA");
        
        int minIndex = 0;
        if(taaIndex == -1 || (tagIndex != -1 && tagIndex < taaIndex)) {
               minIndex = tagIndex;
	} 
	else {
	       minIndex = taaIndex;
	}

	if(minIndex == -1 || (tgaIndex != -1 && tgaIndex < minIndex)) {
		minIndex = tgaIndex;
	}

	if(minIndex == -1) {
		return "";
	}

	return dna.substring(startIndex, minIndex);
        
    }
    
    public int countGenes(String dna){
        int genCount = 0;
        String findGenS = findGene(dna);
        while (true){
            
            if (findGenS.isEmpty()){
                break;
            }
            int nextIndex = dna.indexOf(findGenS);
            String newGenS = dna.substring(nextIndex + 1);
            System.out.println("****" + newGenS);
            findGenS = findGene(newGenS);
            genCount += 1;
            System.out.println(findGenS);
        }
        return genCount;
    }
    
    public void printAllGenes(String dna) {
	while (true) {
	    String gene = findGene(dna);
	    if (gene.isEmpty()) {
		break;
            } else {
		System.out.println(gene);
            }

	}
    }
    
    public void testCountGenes(){
        String dna = "“ATGTAAGATGCCCTAGT”";
        int count = 0;
        count = countGenes(dna);
        System.out.println(count);
    }
}
