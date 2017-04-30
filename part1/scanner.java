import java_cup.runtime.*;


/**
 * Lexical analyser for Question 2 Part I.
 *
 * @author Tomasz Knapik
 */
public class scanner {
    /**
     * Last consumed character.
     */
    protected static int next_char;

    /**
     * Consume one character.
     *
     * <p>
     * Reads character from {@link System#in} and adds it to
     * {@link next_char}.
     * </p>
     *
     * @throws  java.io.IOException;
     */
    protected static void advance() throws java.io.IOException {
        next_char = System.in.read();
    }

    /**
     * Initialise scanner.
     */
    public static void init() throws java.io.IOException {
        advance();
    }

    /**
     * Recognize and return the next complete token
     **/
    public static Symbol next_token() throws java.io.IOException {
        while (true) {
            switch (next_char) {
                case 'k':
                    advance();

                    return new Symbol(sym.VAR_K);

                case 'n':
                    advance();

                    return new Symbol(sym.VAR_N);

                case '1':
                    advance();

                    return new Symbol(sym.TRUE);

                case '0':
                    advance();

                    return new Symbol(sym.FALSE);

                case '?':
                    advance();

                    return new Symbol(sym.UNKNOWN);

                case '&':
                    advance();

                    return new Symbol(sym.AND);

                case '+':
                    advance();

                    return new Symbol(sym.OR);

                case '!':
                    advance();

                    return new Symbol(sym.NOT);

                // Ignore whitespaces
                case ' ':
                case '\n':
                case '\t':
                case '\r':
                    advance();
                    break;

                case -1:
                    return new Symbol(sym.EOF);

                default:
                    String msg = "Invalid character: \""
                                 + (char) next_char
                                 + "\"";
                    throw new Error(msg);
            }
        }
    }
}

