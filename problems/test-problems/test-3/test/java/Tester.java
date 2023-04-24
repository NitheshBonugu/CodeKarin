package main;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class Tester {
	
	@Test

	
	public void findMax_test() {

		Code x = new Code();

		
		int c = x.findMax(23, 37);


		assertEquals(37, c);
	}
}


