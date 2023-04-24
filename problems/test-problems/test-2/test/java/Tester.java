package main;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;


public class Tester {
	
	@Test
	
	
	public void calculateAverage_test() {

		Code x = new Code();
		
		int res = x.avg(10, 19, 61);
		assertEquals(30, res);

	}
	
}