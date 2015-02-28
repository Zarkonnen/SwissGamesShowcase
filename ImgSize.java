import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;

public class ImgSize {
    public static void main(String[] args) throws Exception {
        BufferedImage b = ImageIO.read(new File(args[0]));
        System.out.println(b.getWidth() + " " + b.getHeight());
    }
}
