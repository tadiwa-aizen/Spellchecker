import java.util.*;
import java.io.*;
public class Probabilities{
	static String next = "";
	static ArrayList<TriFreq> arrNext;
	static TriNext tn;

	public HashMap<String, TriNext> getProbMap() {
		HashMap<String, TriNext> mapTri = new HashMap<String, TriNext>(); //hashmap to store TriNext object;
		try {
			File file = new File("probabilities.txt");
			if(! file.exists()) {
				System.out.println("The file probabilitites.txt does not exist.");
				System.exit(0);
			}
			HashMap<String, Integer> map;  //hashmap to get frequency of a trigram
			ArrayList<String> triArr;
			Scanner sc = new Scanner(new FileInputStream(file), "UTF-8");
			while(sc.hasNextLine()) {
				String line = sc.nextLine();
				triArr = new ArrayList<String>();
				map = new HashMap<String, Integer>();
				Scanner scTri = new Scanner(line);
				String tri;
				tri = scTri.next();
				while(scTri.hasNext()) {
					String tNext = scTri.next().trim();
					int freq = scTri.nextInt();
					triArr.add(tNext);
					map.put(tNext, freq);
				}
				scTri.close();
				TriNext tn = new TriNext(triArr, map);
				mapTri.put(tri, tn);
			}
			sc.close();
		}
		catch(Exception e) {
			e.printStackTrace();
		}
		return mapTri;
	}
	
	static boolean upperCase(String s) {
		
		for(char c : s.toCharArray()) {
			if(!Character.isUpperCase(c))
				return false;
		}
		
		return true;
	}
}
