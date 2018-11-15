
/**
 * 在这里给出对类 Part1 的描述。
 * 
 * @作者（你的名字）
 * @版本（一个版本号或者一个日期）
 */
import edu.duke.*;
import org.apache.commons.csv.*;

public class Part1 {
    public void tester (){
        FileResource fr = new FileResource();
        CSVParser parser = fr.getCSVParser();
        for (CSVRecord record : parser){
            System.out.println(record.get("Name"));
        }
    }
    
    public String countryInfo (CSVParser parser, String country){
        String check = "";
        //FileResource fr = new FileResource();
        //parser = fr.getCSVParser();
        for (CSVRecord record : parser){
            String conutr = record.get("Country");
            if ( conutr.contains(country)){
                System.out.print(record.get("Country") + ":");
                System.out.print(record.get("Exports") + ":");
                System.out.println(record.get("Value (dollars)"));
                check = record.get("Country") + ":" + record.get("Exports") + ":" +record.get("Value (dollars)"); 
                return check;
            }
        }
        //if (check.isEmpty()){
        //    return "NOT FOUND";
        //}
        //else{
        //    return check;
        //}
        return "NOT FOUND";
    }
    
    public void listExportersTwoProducts(CSVParser parser, String exportItem1, String exportItem2){
        for (CSVRecord record : parser){
            String expitem = record.get("Exports");
            if ( expitem.indexOf(exportItem1) != -1 && expitem.indexOf(exportItem2) != -1){
                System.out.println(record.get("Country"));
            }
        }
    }
    
    public int numberOfExporters(CSVParser parser, String exportItem){
        int count = 0;
        
        for (CSVRecord record : parser){
            String expitem = record.get("Exports");
            //System.out.println("****" + expitem.contains(exportItem));
            if (expitem.contains(exportItem)){
                System.out.println(record.get("Country"));
                count++;
            }
        }
        return count;
    }
    
    public void bigExporters(CSVParser parser, String amount){
        for (CSVRecord record : parser){
            String value = record.get("Value (dollars)");
            //System.out.println("****" + expitem.contains(exportItem));
            //System.out.println("value length" + value.length() + "amount length" + amount.length());
            if (value.length() > amount.length()){
                System.out.println(record.get("Country") + ": " +  record.get("Value (dollars)"));
                
            }
        }
    }
    
    public void testering() {
        FileResource fr = new FileResource();
        CSVParser parse = fr.getCSVParser();
        //String info = countryInfo(parse, "Nauru");
        
        //System.out.println(info);
        //listExportersTwoProducts(parse, "fish", "nuts");
        int count = numberOfExporters(parse, "sugar");
        System.out.println(count);
        //bigExporters(parse, "$999,999,999,999");
    }
    

    
}
