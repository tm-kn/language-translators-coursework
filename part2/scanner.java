import java.util.ArrayList;
import java.util.Stack;

import java_cup.runtime.*;


public class scanner {
    /* single lookahead character */
    protected static int next_char;
    
    protected static Stack<Integer> nextChars = new Stack<Integer>();

    protected static ArrayList<Integer> history = new ArrayList<Integer>();

    /* advance input by one character */
    protected static void advance()  throws java.io.IOException {
        if (!nextChars.empty()) {
            int nextChar = nextChars.pop();
            history.add(nextChar);
        }

        if (nextChars.empty()) {        
            next_char = System.in.read();
            history.add(next_char);
        }
    }

    protected static void goBackBy(int steps) {
        for (int i = 0; i < steps; i++) {
            int lastEntry = history.remove(history.size() - 1);

            nextChars.push(lastEntry);
        }
    }

    protected static int getNextChar() {
        if (nextChars.empty()) {
            return next_char;
        }
        
        return nextChars.peek();
    }

    protected static boolean analyseMultiCharacterToken(int[] nextTokens) throws java.io.IOException {
       int i = 0;

       for(int token : nextTokens) { 
            advance();
            i++;

            if (getNextChar() != token) {
                goBackBy(i);
                return false;
            }
        }

        return true;
    }

    /* initialize the scanner */
    public static void init() throws java.io.IOException {
        advance();
    }

    /* recognize and return the next complete token */
    public static Symbol next_token()
        throws java.io.IOException
        {
            for (;;) {
                switch (getNextChar())
                {
                    case 'w':

                        // Make sure the scanner does not repeat itself trying to check "wr" forever.
                        if (nextChars.empty() || (!nextChars.empty() && nextChars.peek() == 'r')) {
                            int[] writeTokens = new int[]{'r', 'i', 't', 'e', ' '};

                            if (analyseMultiCharacterToken(writeTokens)) {
                                return new Symbol(sym.WRITE);
                            } else {
                                // Return "w" on top of the stack
                                goBackBy(1);
                                break;
                            }
                        } else {
                            throw new Error("You can only start \"write\" with \"w\"");
                        }
                        
                    case 'k':
                    case 'n':
                        String variableName = String.valueOf((char) getNextChar());

                        advance();
                        
                        return new Symbol(sym.ID, variableName);

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

                    case '=':
                        advance();

                        return new Symbol(sym.ASSIGN);
                    
                    case '(':
                        advance();

                        return new Symbol(sym.LBRACKET);

                    case ')':
                        advance();

                        return new Symbol(sym.RBRACKET);

                    case ';':
                        advance();

                        return new Symbol(sym.SEPARATOR);
                        

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
                        String tokens = "";

                        if (!nextChars.empty()) {
                            for (int token : nextChars) {
                                tokens = (char) token + tokens;
                            }
                        } else {
                            tokens = "w";
                        }

                        throw new Error("Invalid character(s): \"" + tokens + "\"");
                }
            }
        }
};

