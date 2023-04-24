package main;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class Tester {

  @Test
  public void testProperty() {
    Code a = new Code();
    int res = a.add(1, 2);
    assertEquals(3, res);
  }
}
