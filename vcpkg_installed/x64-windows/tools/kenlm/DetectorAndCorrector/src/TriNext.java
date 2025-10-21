import java.io.Serializable;
import java.util.*;

public class TriNext implements Serializable{
	private ArrayList<String> array;
	private HashMap<String, Integer> map;

	TriNext(ArrayList<String> arr, HashMap<String, Integer> hash){
		this.array = arr;
		this.map = hash;
	}
	
	ArrayList<String> getArray(){
		return this.array;
	}
	
	HashMap<String, Integer> getMap(){
		return this.map;
	}
}
