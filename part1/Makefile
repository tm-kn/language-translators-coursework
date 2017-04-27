default: compile

compile:
	java java_cup.Main < parser.cup
	javac parser.java

test:
	python3 unit_tests/tests.py

clean:
	rm -f *.class
	rm -f sym.java
	rm -f parser.java
