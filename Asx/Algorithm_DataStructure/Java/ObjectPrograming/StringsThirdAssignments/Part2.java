import edu.duke.*;


public class Part2 {
    public int findStopCodon(String dna, int startIndex, String stopCodon) {
		int currIndex = dna.indexOf(stopCodon, startIndex + 3);
		while(currIndex != -1) {
			int diff = currIndex - startIndex;
			if(diff % 3 == 0) {
				return currIndex;
			} else {
				currIndex = dna.indexOf(stopCodon, currIndex + 1);
			}
		}

		return -1;
    }
    
    public String findGene(String dna, int where) {
		int startIndex = dna.indexOf("ATG", where);
		if(startIndex == -1 || where == -1) {
			return "";
		}

		int taaIndex = findStopCodon(dna, startIndex, "TAA");
		int tagIndex = findStopCodon(dna, startIndex, "TAG");
		int tgaIndex = findStopCodon(dna, startIndex, "TGA");

		int minIndex = 0;
		
		if(taaIndex == -1 || (tgaIndex != -1 && tgaIndex < taaIndex)) {
			minIndex = tgaIndex;
		} else {
			minIndex = taaIndex;
		}

		if(minIndex == -1 || (tagIndex != -1 && tagIndex < minIndex)) {
			minIndex = tagIndex;
		}

		if(minIndex == -1) {
			return "";
		}
		
		return dna.substring(startIndex, minIndex + 3);
    }
    
    public StorageResource getAllGenes(String dna) {
		StorageResource sr = new StorageResource();
		int startIndex = 0;
		while (true) { 
			String gene = findGene(dna, startIndex);
			
			if (gene == "") {
				break;
			}
			
			sr.add(gene);

			startIndex = dna.indexOf(gene, startIndex) + gene.length();

		}
		return sr;
    }
    
    public double cgRatio (String dna) {
        
        double charRatio = 0.0;
        double stringLen = dna.length();
        
        for (int i = 0; i < stringLen; i++){
            if (dna.charAt(i) == 'C' || dna.charAt(i) == 'G'){
                charRatio += 1;
            }
        }
        
        double ratio = charRatio / stringLen;
        return ratio;
    }
    
    public void processGenes(){
        
        String Longest = "";
	FileResource fr = new FileResource("brca1line.fa");
	String dna = fr.asString().toUpperCase();
	StorageResource sr = getAllGenes(dna);
	int srlongerthan9 = 0;
	int ratiomorethan35 = 0;
	int maxLength = 0;
	for (String s : sr.data()){
	    if (s.length() > 60){
	        System.out.println("***" + s);
	        srlongerthan9 += 1;
	    }
	    if (cgRatio(s) > 0.35){
	        System.out.println("&&&&" + s);
	        ratiomorethan35 += 1;
	    }
	    int lengthtmp = s.length();
	    if (lengthtmp > maxLength){
	        maxLength = lengthtmp;
	        Longest = s;
	    }
	}
	System.out.println("number of s more than 9 is " + srlongerthan9);
	System.out.println("ratio of s more than 35 is " + ratiomorethan35);
	System.out.println("max length is " + maxLength + "the gen is " + Longest);
	System.out.println("length of sr is " + sr.size());
    }
}