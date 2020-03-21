#!/bin/sh

echo "Executing example.py"
echo

echo "Execution time:"
time python3 example.py > ./tests/tmp-example-execution-output.txt
echo

echo "Output:"
cat example-execution-output.txt
echo

#load to compare
REAL_OUTPUT=$(cat ./tests/tmp-example-execution-output.txt)
EXPECTED_OUTPUT=$(cat ./tests/example-expected-output.txt)

# cleanup
rm ./tests/tmp-example-execution-output.txt

#compare and return exit code of 0 - success or 1 - failure
if [ "$REAL_OUTPUT" == "$EXPECTED_OUTPUT" ]
then
  echo "Test passed - Output is correct"
  exit 0
else
  echo -e "Test failed - Output is NOT correct. Expected:"
  cat example-expected-output.txt
  exit 1
fi