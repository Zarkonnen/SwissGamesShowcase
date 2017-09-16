import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;

public class Resize {
    public static void main(String[] args) throws Exception {
        BufferedImage b = ImageIO.read(new File(args[0]));
        int w = Integer.parseInt(args[1]);
        int h = Integer.parseInt(args[2]);
        double targetAspect = 1.0 * w / h;
        double sourceAspect = 1.0 * b.getWidth() / b.getHeight();
        int x = 0;
        int y = 0;
        int tw = w;
        int th = h;
        if (sourceAspect > targetAspect) {
            // Want to cut off the sides.
            tw = (int) Math.ceil(1.0 * b.getWidth() * h / b.getHeight());
            x = w / 2 - tw / 2;
        } else if (sourceAspect < targetAspect) {
            // Want to cut off top and bottom.
            th = (int) Math.ceil(1.0 * b.getHeight() * w / b.getWidth());
            y = h / 2 - th / 2;
        }
        BufferedImage b2 = new BufferedImage(w * 10, h * 10, args[4].equals("png") ? BufferedImage.TYPE_INT_ARGB : BufferedImage.TYPE_3BYTE_BGR);
        b2.getGraphics().drawImage(b, x * 10, y * 10, tw * 10, th * 10, null);
        BufferedImage b3 = new BufferedImage(w, h, args[4].equals("png") ? BufferedImage.TYPE_INT_ARGB : BufferedImage.TYPE_3BYTE_BGR);
        b23.getGraphics().drawImage(b2, 0, 0, w, h, null);
        ImageIO.write(b3, args[4], new File(args[3]));
    }
}
