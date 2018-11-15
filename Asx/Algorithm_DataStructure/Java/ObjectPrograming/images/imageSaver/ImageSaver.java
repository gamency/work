/**
 * Make copies of all images selected within a directory (or folder).
 * 
 * @author Duke Software Team 
 */
import edu.duke.*;
import java.io.File;

public class ImageSaver {
    public void doSave() {
        DirectoryResource dr = new DirectoryResource();
        for (File f : dr.selectedFiles()) {
            ImageResource image = new ImageResource(f);
            String fname = image.getFileName();
            String newName = "gray-" + fname;
            image.setFileName(newName);
            image.draw();
            image.save();
        }
    }
    
    public ImageResource makeGray(ImageResource inImage) {
        //I made a blank image of the same size
        ImageResource outImage = new ImageResource(inImage.getWidth(), inImage.getHeight());
        //for each pixel in outImage
        for (Pixel pixel: outImage.pixels()) {
            //look at the corresponding pixel in inImage
            Pixel inPixel = inImage.getPixel(pixel.getX(), pixel.getY());
            //compute inPixel's red + inPixel's blue + inPixel's green
            //divide that sum by 3 (call it average)
            int average = (inPixel.getRed() + inPixel.getBlue() + inPixel.getGreen())/3;
            //set pixel's red to average
            pixel.setRed(average);
            //set pixel's green to average
            pixel.setGreen(average);
            //set pixel's blue to average
            pixel.setBlue(average);
        }
        //outImage is your answer
        return outImage;
    }
    
    public ImageResource makeInvert(ImageResource inImage) {
        //I made a blank image of the same size
        ImageResource outImage = new ImageResource(inImage.getWidth(), inImage.getHeight());
        //for each pixel in outImage
        for (Pixel pixel: outImage.pixels()) {
            //look at the corresponding pixel in inImage
            Pixel inPixel = inImage.getPixel(pixel.getX(), pixel.getY());
            //compute inPixel's red + inPixel's blue + inPixel's green
            //divide that sum by 3 (call it average)
            int average = (inPixel.getRed() + inPixel.getBlue() + inPixel.getGreen())/3;
            //set pixel's red to average
            int full = 255;
            int redInt = full - inPixel.getRed() ;
            int greenInt = full -inPixel.getGreen() ;
            int blueInt = full -inPixel.getBlue();
            int inv = average - full;
            
            System.out.println("****" + inPixel.getRed() + " " + redInt);
            
            pixel.setRed(255 - inPixel.getRed());
            //set pixel's green to average
            pixel.setGreen(255 - inPixel.getGreen());
            //set pixel's blue to average
            pixel.setBlue(255 - inPixel.getBlue());
            
            //System.out.println("****" + inPixel.getRed() + inPixel.getBlue());
        }
        //outImage is your answer
        return outImage;
    }
    
    public void selectAndConvert () {
	DirectoryResource dr = new DirectoryResource();
	for (File f : dr.selectedFiles()) {
	    ImageResource inImage = new ImageResource(f);
	    ImageResource gray = makeGray(inImage);
	    //gray.draw();
	    //ImageResource image = new ImageResource(f);
            String fname = inImage.getFileName();
            String newName = "gray-" + fname;
            gray.setFileName(newName);
            gray.save();
        }
    }
    
    public void makeInvertnsave () {
	DirectoryResource dr = new DirectoryResource();
	for (File f : dr.selectedFiles()) {
	    ImageResource inImage = new ImageResource(f);
	    ImageResource invert = makeInvert(inImage);
	    //gray.draw();
	    //ImageResource image = new ImageResource(f);
            String fname = inImage.getFileName();
            String newName = "invert-" + fname;
            invert.setFileName(newName);
            invert.save();
        }
    }
}
