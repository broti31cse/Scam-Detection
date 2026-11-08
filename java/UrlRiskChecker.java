public class UrlRiskChecker {

    public static void main(String[] args) {

        String url = args.length > 0
                ? args[0]
                : "http://example-login.test";

        int score = 0;

        String lower = url.toLowerCase();

        if (lower.startsWith("http://"))
            score += 20;

        if (lower.contains("@"))
            score += 25;

        if (lower.contains("login") ||
            lower.contains("password") ||
            lower.contains("verify"))
            score += 15;

        System.out.println("TrustShield Java Scanner");

        System.out.println("URL: " + url);

        System.out.println("Risk Score: " + score);

        if (score >= 50)
            System.out.println("High Risk");

        else if (score >= 20)
            System.out.println("Needs Caution");

        else
            System.out.println("Lower Risk");
    }
}
