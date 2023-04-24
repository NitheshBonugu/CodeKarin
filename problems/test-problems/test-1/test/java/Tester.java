package main;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;


public class Tester {
	
	@Test
	
	
	public void calPower_test() {

		Code x = new Code();
		
		double res = x.calPower(2, 5);
		assertEquals(32.0, res);

	}
	
}