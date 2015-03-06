import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;

public class Resize {
    public static void main(String[] args) throws Exception {
        BufferedImage b = ImageIO.read(new File(args[0]));
        int size = Integer.parseInt(args[1]);
        int w, h;
        if (b.getWidth() > b.getHeight()) {
            w = 300;
            h = 300 * b.getHeight() / b.getWidth();
        } else {
            h = 300;
            w = 300 * b.getWidth() / b.getHeight();
        }
        BufferedImage b2 = new BufferedImage(w, h, args[3].equals("png") ? BufferedImage.TYPE_INT_ARGB : BufferedImage.TYPE_3BYTE_BGR);
        b2.getGraphics().drawImage(b, 0, 0, w, h, null);
        ImageIO.write(b2, args[3], new File(args[2]));
    }
}
