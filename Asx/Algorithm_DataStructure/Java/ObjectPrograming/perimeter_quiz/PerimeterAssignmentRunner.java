import edu.duke.*;
import java.io.File;

public class PerimeterAssignmentRunner {
    public double getPerimeter (Shape s) {
        // Start with totalPerim = 0
        double totalPerim = 0.0;
        // Start wth prevPt = the last point 
        Point prevPt = s.getLastPoint();
        // For each point currPt in the shape,
        for (Point currPt : s.getPoints()) {
            // Find distance from prevPt point to currPt 
            double currDist = prevPt.distance(currPt);
            // Update totalPerim by currDist
            totalPerim = totalPerim + currDist;
            // Update prevPt to be currPt
            prevPt = currPt;
        }
        // totalPerim is the answer
        return totalPerim;
    }

    public int getNumPoints (Shape s) {
        // Put code here
        int num = 0;
        for (Point p : s.getPoints()){
            num += 1;
        }
        return num;
    }

    public double getAverageLength(Shape s) {
        // Put code here
        Point prevPt = s.getLastPoint();
        double totalDist = 0.0;
        //getPerimeter
        for (Point currPt: s.getPoints()){
            double currDist = prevPt.distance(currPt);
            totalDist += currDist;
            prevPt = currPt;
        }
        int numPoints = getNumPoints(s);
        return totalDist / numPoints;
    }

    public double getLargestSide(Shape s) {
        // Put code here
        Point prevPt = s.getLastPoint();
        double longestSlide = 0;
        for (Point currPt : s.getPoints()){
            double currDist = prevPt.distance(currPt);
            if (currDist > longestSlide){
                longestSlide = currDist;
            }
            prevPt = currPt;
        }
        return longestSlide;
    }

    public double getLargestX(Shape s) {
        // Put code here
        Point prevPt = s.getLastPoint();
        
        double largestX = prevPt.getX();
        
        for (Point currPt : s.getPoints()){
            double pointx = prevPt.getX();
            if (pointx > largestX){
                largestX = pointx;
            }
            prevPt = currPt;
        }
        
        return largestX;
    }

    public double getLargestPerimeterMultipleFiles() {
        // Put code here
        DirectoryResource dr = new DirectoryResource();
        File lagestFile = null;
        double largestPerimeter = 0.0;
        for (File f: dr.selectedFiles()){
            FileResource fr = new FileResource(f);
            Shape s = new Shape(fr);
            double perimeter = getPerimeter(s);
            System.out.println("**** perimeter is " + perimeter);
            if (largestPerimeter < perimeter){
                largestPerimeter = perimeter;
                System.out.println("perimeter is " + largestPerimeter);
                lagestFile = f;
            }
            
        }
        System.out.println("*****" + lagestFile.getName());
        return largestPerimeter;
    }

    public String getFileWithLargestPerimeter() {
        // Put code here
        //File temp = null;    // replace this code
        DirectoryResource dr = new DirectoryResource();
        File lagestFile = null;
        double largestPerimeter = 0.0;
        for (File f: dr.selectedFiles()){
            FileResource fr = new FileResource(f);
            Shape s = new Shape(fr);
            double perimeter = getPerimeter(s);
            System.out.println("**** perimeter is " + perimeter);
            if (largestPerimeter < perimeter){
                largestPerimeter = perimeter;
                System.out.println("perimeter is " + largestPerimeter);
                lagestFile = f;
            }
            
        }
        //System.out.println("*****" + lagestFile.getName());

        return lagestFile.getName();
    }

    public void testPerimeter () {
        FileResource fr = new FileResource();
        Shape s = new Shape(fr);
        double length = getPerimeter(s);
        System.out.println("perimeter = " + length);
        int numPoints = getNumPoints(s);
        System.out.println("points number of shape is " + numPoints);
        double averageLength = getAverageLength(s);
        System.out.println("average length of shape is " + averageLength);
        double longestSlide = getLargestSide(s);
        System.out.println("lagest length of shape is " + longestSlide);
        double lagestX = getLargestX(s);
        System.out.println("lagest x of shape is " + lagestX);
    }
    
    public void testPerimeterMultipleFiles() {
        // Put code here
        double largestPerimeter = getLargestPerimeterMultipleFiles();
        System.out.println("largest perimeter of these file is " + largestPerimeter);
    }

    public void testFileWithLargestPerimeter() {
        // Put code here
        String file = getFileWithLargestPerimeter();
        System.out.println("largest perimeter file name is " + file);
    }

    // This method creates a triangle that you can use to test your other methods
    public void triangle(){
        Shape triangle = new Shape();
        triangle.addPoint(new Point(0,0));
        triangle.addPoint(new Point(6,0));
        triangle.addPoint(new Point(3,6));
        for (Point p : triangle.getPoints()){
            System.out.println(p);
        }
        double peri = getPerimeter(triangle);
        System.out.println("perimeter = "+peri);
    }

    // This method prints names of all files in a chosen folder that you can use to test your other methods
    public void printFileNames() {
        DirectoryResource dr = new DirectoryResource();
        for (File f : dr.selectedFiles()) {
            System.out.println(f);
        }
    }

    public static void main (String[] args) {
        PerimeterAssignmentRunner pr = new PerimeterAssignmentRunner();
        //pr.testPerimeter();
        //pr.printFileNames();
        //pr.testPerimeterMultipleFiles();
        pr.testFileWithLargestPerimeter();
    }
}
