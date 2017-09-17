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
        int sw = b.getWidth();
        int sh = b.getHeight();
        int tx = 0;
        int ty = 0;
        int tw = b.getWidth();
        int th = b.getHeight();
        if (sourceAspect > targetAspect) {
            // Want to cut off the sides.
            tw = w * th / h;
            tx = tw / 2 - sw / 2;
        } else if (sourceAspect < targetAspect) {
            // Want to cut off top and bottom.
            th = h * tw / w;
            ty = th / 2 - sh / 2;
        }
        BufferedImage b2 = new BufferedImage(tw, th, args[4].equals("png") ? BufferedImage.TYPE_INT_ARGB : BufferedImage.TYPE_3BYTE_BGR);
        b2.getGraphics().drawImage(b, tx, ty, null);
        ImageIO.write(b2, args[4], new File(args[3]));
    }
}
