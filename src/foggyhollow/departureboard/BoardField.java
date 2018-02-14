package foggyhollow.departureboard;

import java.net.URL;
import jmri.jmrit.catalog.NamedIcon;
import jmri.jmrit.display.Editor;
import jmri.jmrit.display.MemoryIcon;

public class BoardField
{
    String imagePath = "/flip/tiny/";
    
    public BoardField(int startColumn, int numColumns, boolean isNumeric, Editor editor, String memoryName)
    {
        for (int i=0; i<numColumns; i++)
        {
            MemoryIcon icon = new MemoryIcon("IM" + memoryName + Integer.toString(i), editor);            
            for (int c=0; c<26; c++)
            {
                char value = (char) (c + (int) 'A');
                String columnIconImage = "flip-" + (char)value + ".png";
                try
                {
                    URL imageURL = new URL(imagePath + columnIconImage.toLowerCase());
                    NamedIcon nmi = new NamedIcon(imageURL, Character.toString(value));
                    icon.addKeyAndIcon(nmi, Character.toString(value));                    
                }
                catch (Exception err)
                {
                    err.printStackTrace();
                }
            }
        }
    }

}
