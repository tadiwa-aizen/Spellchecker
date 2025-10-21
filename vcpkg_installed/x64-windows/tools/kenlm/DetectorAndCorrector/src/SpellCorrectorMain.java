import java.io.*;
import java.util.*;

public class SpellCorrectorMain {
    public static void main(String[] args) {
        try {
            BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
            String word = reader.readLine();
            
            ErrorCorrector corrector = new ErrorCorrector();
            corrector.initCorrector();
            ArrayList<String> corrections = corrector.correct(word);
            
            // Output only the JSON array
            System.out.print("[");
            for (int i = 0; i < corrections.size(); i++) {
                if (i > 0) System.out.print(",");
                System.out.print("\"" + corrections.get(i) + "\"");
            }
            System.out.println("]");
            
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            System.exit(1);
        }
    }
} 