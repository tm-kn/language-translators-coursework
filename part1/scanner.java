import java_cup.runtime.*;


public class scanner {
    /* single lookahead character */
    protected static int next_char;

    /* advance input by one character */
    protected static void advance()
        throws java.io.IOException
        { next_char = System.in.read(); }

    /* initialize the scanner */
    public static void init()
        throws java.io.IOException
        { advance(); }

    /* recognize and return the next complete token */
    public static Symbol next_token()
        throws java.io.IOException
        {
            for (;;) {
                switch (next_char)
                {
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
                        throw new Error("Invalid character: \"" + (char) next_char + "\"");    
                }
            }
        }
};

