.DEFAULT: test
.PHONY: run test clean deploy

MIRROR = rsync -avz --rsh=ssh --delete --exclude=.git --exclude=ucas.ini

run:
	./server.py

test:
	./ucas.py

clean:
	$(RM) *.pyc

deploy:
	$(MIRROR) . rmm@severn.cs.nott.ac.uk:/lhome/rmm/src/ucas-www
	ssh rmm@severn.cs.nott.ac.uk \
		"( cd ~/src/ucas-www &&  \
			source ~/localpy/bin/activate && make run )"
