.DEFAULT: test
.PHONY: run test clean deploy

MIRROR = rsync -avz --rsh=ssh --delete

run:
	./run.py

test:
	./ucas.py

clean:
	$(RM) *.pyc

deploy:
	$(MIRROR) rmm@severn.cs.nott.ac.uk:/lhome/rmm/src/ucas-webapp
	ssh rmm@severn.cs.nott.ac.uk "( cd ~/src/ucas-webapp && make run )"
