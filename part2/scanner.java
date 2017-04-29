import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.Stack;

import java_cup.runtime.*;


public class scanner {
    /* single lookahead character */
    protected static int next_char;
    
    protected static Stack<Integer> nextChars = new Stack<Integer>();

    protected static List<Integer> history = new ArrayList<Integer>();

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

    /**
     * Get items from history and puts them back on the stack (nextChars) to be consumed by number of entries.
     * Deletes entries from the history.
     */
    protected static void goBackBy(int steps) {
        for (int i = 0; i < steps; i++) {
            int lastEntry = history.remove(history.size() - 1);

            nextChars.push(lastEntry);
        }
    }
    
    /**
     * Get the character that is being iterated over.
     */
    protected static int getNextChar() {
        // If there're any characters in nextChars stack, use them first.
        if (nextChars.empty()) {
            return next_char;
        }
        
        return nextChars.peek();
    }
    
    /**
     * Give it a characters array and check whether it matches the programme.
     */
    protected static boolean analyseMultiCharacterToken(int[] nextTokens)
                throws java.io.IOException {
       int i = 0;

       for(int token : nextTokens) { 
            advance();
            i++;

            if (getNextChar() != token) {
                goBackBy(i);
                return false;
            }
        }

        advance();

        return true;
    }

    /* initialize the scanner */
    public static void init() throws java.io.IOException {
        advance();
    }
    
    /**
     * Get variable name out of the programme input.
     */
    public static String parseVariableName(char letter)
            throws java.io.IOException {
        int[] allowedStringNameCharactersArray = new int[]{
            // Lower-case letters
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y', 'z',

            // Special characters
            '_'
        };
        
        // Convert array to Set so we can use contains() method
        Set<Integer> allowedCharactersSet = new HashSet<Integer>();

        for (int allowedCharacter: allowedStringNameCharactersArray)
            allowedCharactersSet.add(allowedCharacter);

        String stringName = String.valueOf((char) letter);
        
        // Move onto next character (currently we're at the first charactter of the variable name
        advance();
        
        // Append every next character form input as long as it is a valid character for a variable name
        while (allowedCharactersSet.contains(getNextChar())) {
            stringName += getNextChar();
            advance();
        }
        
        // Cancels the last advance() that outputed invalid symbol so the main parser can handle it
        goBackBy(1);

        return stringName;
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
                        // Variable starting with "w"
                        } else { 
                            String variableName = parseVariableName((char) getNextChar());
                            
                            return new Symbol(sym.ID, variableName);
                        }
                    
                    case '-':
                        
                        // Make sure the scanner does not repeat itself trying to check "->" forever.
                        if (nextChars.empty() || (!nextChars.empty() && nextChars.peek() == '>')) {
                            int[] writeTokens = new int[]{'>'};

                            if (analyseMultiCharacterToken(writeTokens)) {
                                return new Symbol(sym.IMPLY);
                            } else {
                                // Return "-" on top of the stack
                                goBackBy(1);
                                break;
                            }
                        } else {
                            throw new Error("You can only start \"->\" with \"-\"");
                        }

                    case 'a': case 'b': case 'c': case 'd':
                    case 'e': case 'f': case 'g': case 'h':
                    case 'i': case 'j': case 'k': case 'l':
                    case 'm': case 'n': case 'o': case 'p':
                    case 'q': case 'r': case 's': case 't':
                    case 'u': case 'v': case 'x':
                        String variableName = parseVariableName((char) getNextChar());
                        
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
                            tokens += (char) getNextChar();
                        }

                        throw new Error("Invalid character(s): \"" + tokens + "\"");
                }
            }
        }
};

