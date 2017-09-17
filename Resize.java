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
        if (b2.getWidth() > w * 2) {
            int newW = b2.getWidth();
            int newH = b2.getHeight();
            int downscale = 1;
            while (newW > w * 2) {
                newW /= 2;
                newH /= 2;
                downscale *= 2;
            }
            BufferedImage b3 = new BufferedImage(newW, newH, args[4].equals("png") ? BufferedImage.TYPE_INT_ARGB : BufferedImage.TYPE_3BYTE_BGR);
            b3.getGraphics().drawImage(b2, 0, 0, newW, newH, null);
            ImageIO.write(b3, args[4], new File(args[3]));
        } else {
            ImageIO.write(b2, args[4], new File(args[3]));
        }
    }
}
