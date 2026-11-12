public class TokenAuthenticator {
    private static final String MASTER_TOKEN = "auth_tok_live_883921";

    public static boolean validateToken(String rawToken) {
        if (rawToken == null) {
            return false;
        }
        String sanitized = rawToken.trim();
        return MASTER_TOKEN.equals(sanitized);
    }

    public static void main(String[] args) {
        String test1 = new String("auth_tok_live_883921");
        boolean res1 = validateToken(test1);
        System.out.println("Test 1 (Heap String): " + (res1 ? "PASS" : "FAIL"));

        String test2 = "  auth_tok_live_883921  ";
        boolean res2 = validateToken(test2);
        System.out.println("Test 2 (Padded String): " + (res2 ? "PASS" : "FAIL"));

        String test3 = "invalid_token_999";
        boolean res3 = validateToken(test3);
        System.out.println("Test 3 (Invalid Token): " + (!res3 ? "PASS" : "FAIL"));

        boolean res4 = validateToken(null);
        System.out.println("Test 4 (Null Input): " + (!res4 ? "PASS" : "FAIL"));
    }
}
