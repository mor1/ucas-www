.DEFAULT: test
.PHONY: run test clean deploy

MIRROR = rsync -avz --rsh=ssh --delete \
	--exclude=.git --exclude=ucas.ini --exclude=*.log

RUN = ". ~/localpy/bin/activate \
	&& cd ~/src/ucas-www \
	&& ./server.py 1>ucas.$(date +%Y%m%d-%H%M%S).log 2>&1"

test:
	./ucas.py

clean:
	$(RM) *.pyc

deploy:
	$(MIRROR) . rmm@severn.cs.nott.ac.uk:/lhome/rmm/src/ucas-www
	ssh rmm@severn.cs.nott.ac.uk \
		screen /usr/bin/env bash -c $RUN
