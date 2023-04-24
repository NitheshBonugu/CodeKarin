package main;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;


public class Tester {
	
	@Test
	
	public void majorTCU_test() {

		Code x = new Code();

		String res = x.majorTCU("CS", "TCU");

		assertEquals("CS,TCU", res);

	}
	
}