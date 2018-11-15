/**
 * Print out total number of babies born, as well as for each gender, in a given CSV file of baby name data.
 * 
 * @author Duke Software Team 
 */
import edu.duke.*;
import org.apache.commons.csv.*;
import java.io.*;

public class BabyBirths {
    public void printNames () {
        FileResource fr = new FileResource();
        for (CSVRecord rec : fr.getCSVParser(false)) {
            int numBorn = Integer.parseInt(rec.get(2));
            if (numBorn <= 100) {
                System.out.println("Name " + rec.get(0) +
                           " Gender " + rec.get(1) +
                           " Num Born " + rec.get(2));
            }
        }
    }

    public void totalBirths (FileResource fr) {
        int totalBirths = 0;
        int totalBoys = 0;
        int totalGirls = 0;
        int boyNum = 0;
        int girlNum = 0;
        for (CSVRecord rec : fr.getCSVParser(false)) {
            int numBorn = Integer.parseInt(rec.get(2));
            
            totalBirths += numBorn;
            if (rec.get(1).equals("M")) {
                totalBoys += numBorn;
                boyNum += 1;
            }
            else {
                totalGirls += numBorn;
                girlNum += 1;
            }
        }
        System.out.println("total births = " + totalBirths);
        System.out.println("female girls = " + totalGirls);
        System.out.println("male boys = " + totalBoys);
        System.out.println("number of boys = " + boyNum);
        System.out.println("number of girl = " + girlNum);
        int total = girlNum + boyNum;
        System.out.println("number of total = " + total);
    }
    
    public int getRank(int year, String name, String gender){
        //FileResource fr = new FileResource(String.format("us_babynames/us_babynames_by_year/yob%s.csv", year));
        CSVParser parser = getFileParser(year);
        int i = 0;
        for (CSVRecord rec : parser){
            String name_of_file = rec.get(0);
            i += 1;
            if (name_of_file.equals(name) && rec.get(1).equals(gender)){
                return i;
            }
        }
        return -1;
    }
    
    public String getName(int year, int rank, String gender){
        CSVParser parser = getFileParser(year);
        
        //long currRank = record.getRecordNumber();
        int i = 0;
        for (CSVRecord rec : parser){
            String name_of_file = rec.get(0);
            i += 1;
            if (i == rank && rec.get(1).equals(gender)){
                return rec.get(0);
            }
        }
        return "NO NAME";
    }
    
    public void whatIsNameInYear(String name, int year, int newYear, String gender){
        int nameRank = getRank(year, name, gender);
        if (nameRank == -1){
            System.out.println("no found name");
        }
        else{
            String trName = getName(newYear, nameRank, gender);
            System.out.println(name + "born in " + year + " would be " + trName + " if she was born in " + newYear+ ".");
        }
    }
    
    public int yearOfHighestRank(String name, String gender){
        String fileName = "";
	DirectoryResource dr = new DirectoryResource();
	
	int miniRank = 0;
	int miniyear = 0;
	System.out.println("******");
	int tmpRank = 0;
	for (File f : dr.selectedFiles()){
	    FileResource fr = new FileResource(f);
	    CSVParser parse = fr.getCSVParser(false);
	    
	    fileName = f.getName();
	    fileName = fileName.replaceAll("[^\\d]", "");
	    System.out.println("filename  is  " + fileName);
	    int yeartmp = Integer.parseInt(fileName);
	    //int tmpRank = getRank(yeartmp, name, gender);
	    
	    int i = 0;
	    
            for (CSVRecord rec : parse){
                String name_of_file = rec.get(0);
                i += 1;
                if (name_of_file.equals(name) && rec.get(1).equals(gender)){
                    tmpRank = i;
                }
            }
            
	    
	    System.out.println("yeartmp  is  " + yeartmp);
	    System.out.println("minirank  is  " + miniRank + "tmpRank is" + tmpRank);
	    if (miniRank == 0){
	        miniRank = tmpRank;
	        miniyear = yeartmp;
	    }
	    else{
	        if (miniRank > tmpRank){
	            miniRank = tmpRank;
	            miniyear = yeartmp;
	        }
	    }
	    
	}
	if (miniyear == 0){
	    miniyear = -1;
	}
	return miniyear;
    }
    
    public double getAverageRank(String name, String gender) {
		// Initialize a DirectoryResource
	DirectoryResource dr = new DirectoryResource();
		// Define rankTotal, howMany
	double rankTotal = 0.0;
	int howMany = 0;
		// For every file the directory add name rank to agvRank
	for(File f : dr.selectedFiles()) {
	    FileResource fr = new FileResource(f);
	    CSVParser parser = fr.getCSVParser(false);
	    for(CSVRecord record : parser) {
		String currName = record.get(0);
		String currGender = record.get(1);
		if(currName.equals(name) && currGender.equals(gender)){
		    long currRank = record.getRecordNumber();
		    rankTotal += (double)currRank;
		    howMany += 1;
		}
            }
	}
		// Define avgRank = rankTotal / howMany
	double avgRank = rankTotal / (double)howMany;
	return avgRank;
    }
  
    /*
	* This method returns the total births of the same gender that are ranked higher
	  * than the parameter name
	*/
     public int getTotalBirthsRankedHigher(int year, String name, String gender) {
		int numBorn = 0;
		long rank = getRank(year, name, gender);
		FileResource fr = new FileResource();
		CSVParser parser = fr.getCSVParser(false);
		for(CSVRecord record : parser) {
			int currBorn = Integer.parseInt(record.get(2));
			String currGender = record.get(1);
			long currRank = record.getRecordNumber();
			if(gender.equals(currGender) && rank > currRank) {
				numBorn += currBorn;
			}
		}
		return numBorn;
	}
    
    protected static CSVParser getFileParser(int year) {

        FileResource fr = new FileResource(String.format("us_babynames/us_babynames_by_year/yob%s.csv", year));
        //FileResource fr = new FileResource(String.format("testing/yob%sshort.csv", year));
        return fr.getCSVParser(false);


    }

    public void testTotalBirths () {
        //FileResource fr = new FileResource();
        FileResource fr = new FileResource("data/yob2014.csv");
        totalBirths(fr);
        int rank = getRank(2012, "Mason", "M");
        System.out.println("rank is  " + rank);
    }
    
    public void testGetRank () {
        //FileResource fr = new FileResource();
        //FileResource fr = new FileResource("data/yob2014.csv");
        //totalBirths(fr);
        int rank = getRank(2012, "Mason", "M");
        System.out.println("rank is  " + rank);
    }
    
    public void testName () {
        //FileResource fr = new FileResource();
        //FileResource fr = new FileResource("data/yob2014.csv");
        //totalBirths(fr);
        String rankName = getName(2012, 2, "M");
        System.out.println("name is  " + rankName);
    }
    
    public void testWhatIsNameInYear () {
        //FileResource fr = new FileResource();
        //FileResource fr = new FileResource("data/yob2014.csv");
        //totalBirths(fr);
        whatIsNameInYear("Isabella", 2012, 2014, "F");
        //System.out.println("name is  " + rankName);
        
    }
    
    public void testing(){
        //System.out.println(getAverageRank("Jacob", "M"));
		
	System.out.println(getTotalBirthsRankedHigher(2012, "Ethan", "M"));
    }
    public void testyearOfHighestRank () {
        //FileResource fr = new FileResource();
        //FileResource fr = new FileResource("data/yob2014.csv");
        //totalBirths(fr);
        int year = yearOfHighestRank("Mason", "M");
        System.out.println("year of higheset  is  " + year);
    }
}

