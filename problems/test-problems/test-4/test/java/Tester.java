package main;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;


public class Tester {
	
	@Test
	
	
	public void studentInitial_test() {

		Code x = new Code();

		
		String res = x.studentInitial("N", "B");
		assertEquals("NB", res);

	}
	
}