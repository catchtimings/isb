import java.math.BigInteger;
import java.util.Random;

public class Main {
    public static void main(String[] args) {
        BigInteger number = new BigInteger(128, new Random());
        String binaryString = String.format("%128s", number.toString(2)).replace(' ', '0');
        System.out.println(binaryString);
    }
}
