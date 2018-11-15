
/**
 * 在这里给出对类 Part1 的描述。
 * 
 * @作者（你的名字）
 * @版本（一个版本号或者一个日期）
 */
import edu.duke.*;
import org.apache.commons.csv.*;
import java.io.*;

public class Part1 {
    
    public CSVRecord coldestHourInFile(CSVParser parser){
        CSVRecord codestSoFar = null;
        
        for (CSVRecord currentRow : parser){
            codestSoFar = getCodestOfTwo(currentRow, codestSoFar);
        }
        
        return codestSoFar;
    }
    
    public CSVRecord getCodestOfTwo(CSVRecord currentRow, CSVRecord codestSoFar){
        if (codestSoFar == null){
            codestSoFar = currentRow;
        }
        else{
            double currentTemp = Double.parseDouble(currentRow.get("TemperatureF"));
            double codestTemp = Double.parseDouble(codestSoFar.get("TemperatureF"));
            if (codestTemp > currentTemp){
                codestSoFar = currentRow;
            }
        }
        return codestSoFar;
    }
    
    public void testHottestInDay () {
	FileResource fr = new FileResource("nc_weather/2014/weather-2014-05-01.csv");
	CSVRecord largest = coldestHourInFile(fr.getCSVParser());
	System.out.println("codest temperature was " + largest.get("TemperatureF") +
				   " at " + largest.get("TimeEDT"));
    }
    
    public String fileWithColdestTemperature(){
        File fileName = null;
        CSVRecord coldestTemp = null;
        
        DirectoryResource dr = new DirectoryResource();
        for (File f: dr.selectedFiles()){
            FileResource fr = new FileResource(f);
            CSVParser parser = fr.getCSVParser();
            CSVRecord currRow = coldestHourInFile(parser);
            
            if (coldestTemp == null){
                coldestTemp = currRow;
                fileName = f;
            }
            else{
                double currentTemp = Double.parseDouble(currRow.get("TemperatureF"));
                double codestTemp = Double.parseDouble(coldestTemp.get("TemperatureF"));
                if (codestTemp > currentTemp && currentTemp > -50){
                    coldestTemp = currRow;
                    fileName = f;
                }
            }
            
        }
        return fileName.getAbsolutePath();
    }
    
    public void testFileWithColdestTemperature() {
	String fileWithColdestTemp = fileWithColdestTemperature();
	File f = new File(fileWithColdestTemp);
	String fileName = f.getName();

	System.out.println("Coldest day was in file " + fileName);

		
	FileResource fr = new FileResource(f);
	CSVParser parser = fr.getCSVParser();
	CSVRecord lowestTemp = coldestHourInFile(parser);

	System.out.println("Coldest Temperature is: " + lowestTemp.get("TemperatureF"));

	System.out.println("All the Temperatures on the coldest day were");
	CSVParser parser2 = fr.getCSVParser();
	for(CSVRecord record : parser2) {
		double temp = Double.parseDouble(record.get("TemperatureF"));
		System.out.println(temp);
        }
    }
    
    public CSVRecord lowestHumidityInFile(CSVParser parser){
        CSVRecord codestSoFar = null;
        
        for (CSVRecord currentRow : parser){
            //codestSoFar = getCodestOfTwo(currentRow, codestSoFar);
            if (codestSoFar == null){
                codestSoFar = currentRow;
            }
            else{
                if(!currentRow.get("Humidity").equals("N/A") && !codestSoFar.get("Humidity").equals("N/A")){
                    int currentTemp = Integer.parseInt(currentRow.get("Humidity"));
                    int codestTemp = Integer.parseInt(codestSoFar.get("Humidity"));
                    if (codestTemp > currentTemp){
                        codestSoFar = currentRow;
                    }
                }
            }   
        }
        
        return codestSoFar;
            
    }
    
    public void testLowestHumidityInFile() {
		FileResource fr = new FileResource();
		CSVParser parser = fr.getCSVParser();
		CSVRecord lowestHumdity = lowestHumidityInFile(parser);

		System.out.println(lowestHumdity.get("Humidity") + " at " + lowestHumdity.get("DateUTC"));
     }
    
    public CSVRecord lowestHumidityInManyFiles(){
        CSVRecord lowestHumdity = null;
	int currHumd;
	int lowestHumd;

	DirectoryResource dr = new DirectoryResource();
	for (File f : dr.selectedFiles()) {
		FileResource fr = new FileResource(f);
		CSVParser parser = fr.getCSVParser();
		CSVRecord currRow = lowestHumidityInFile(parser);
			
		if(lowestHumdity == null) {
			lowestHumdity = currRow;
		} 
		else {
			int currTemp = Integer.parseInt(currRow.get("Humidity"));
			int lowestTemp = Integer.parseInt(lowestHumdity.get("Humidity"));
			if(currTemp < lowestTemp) {
				lowestHumdity = currRow;
			}

			else {
				if(currRow.get("Humidity") != "N/A" && lowestHumdity.get("Humidity") != "N/A") {
					currHumd = Integer.parseInt(currRow.get("Humidity"));
					lowestHumd = Integer.parseInt(lowestHumdity.get("Humidity"));
						
					if(currHumd < lowestHumd) {
						lowestHumdity = currRow;
					}
				}
			}
		}
	}
	return lowestHumdity;
    }
    
    public void testLowestHumidityInManyFiles() {
		CSVRecord record = lowestHumidityInManyFiles();
		System.out.println(record.get("Humidity") + " at " + record.get("DateUTC"));
     } 
     
    public double averageTemperatureInFile(CSVParser parser) {
		double num = 0.0;
		double sum = 0.0;

		for(CSVRecord record : parser) {
			double temp = Double.parseDouble(record.get("TemperatureF"));
			sum += temp;
			num++;
		}

		double average = sum / num;
		return average;
	}

	public void testAverageTemperatureInFile() {
		FileResource fr = new FileResource();
		CSVParser parser = fr.getCSVParser();
		double avg = averageTemperatureInFile(parser);

		System.out.println("average temperature is " + avg);
	}

	public double averageTemperatureWithHighHumidityInFile(CSVParser parser, int value) {
		double num = 0.0;
		double sum = 0.0;

		for(CSVRecord record : parser) {
			double temp = Double.parseDouble(record.get("TemperatureF"));
			int humidity = Integer.parseInt(record.get("Humidity"));
			if(humidity >= value) {
				sum += temp;
				num++;
			}
		}

		double average = sum / num;
		return average;
	}

	public void testAverageTemperatureWithHighHumidityInFile() {
		FileResource fr = new FileResource();
		CSVParser parser = fr.getCSVParser();
		double avg = averageTemperatureWithHighHumidityInFile(parser, 80);

		if(!Double.isNaN(avg)) {
			System.out.println("****average temperature is " + avg);
		} else {
			System.out.println("No Temperature was found");
		}
	}
}
