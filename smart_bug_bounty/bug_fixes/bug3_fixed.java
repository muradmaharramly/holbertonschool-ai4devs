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
        String incomingHeader = new String("auth_tok_live_883921");
        boolean authenticated = validateToken(incomingHeader);
        System.out.println("Authenticated: " + authenticated);
    }
}
