for rpyc in `find . -name "*.rpyc"`;
do
	rm -f $rpyc
done;