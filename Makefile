.DEFAULT: test
.PHONY: run test clean deploy stop start mirror

MIRROR = rsync -avz --rsh=ssh --delete \
	--exclude=.git --exclude=ucas.ini --exclude=*.log

STOP = 'bash -c "ps aux | \grep \"^rmm.*python ./server.py\" | \grep -v grep \
		 | tr -s \" \" | cut -d \" \" -f 2 | xargs kill -9"'

RUN = 'bash -c "source ~/localpy/bin/activate \
	&& cd ~/src/ucas-www \
	&& ./server.py 1>ucas.$$(date +%Y%m%d-%H%M%S).log 2>&1"'

test:
	./ucas.py

clean:
	$(RM) *.pyc

stop:
	ssh rmm@severn.cs.nott.ac.uk ${STOP} || true
mirror:
	$(MIRROR) . rmm@severn.cs.nott.ac.uk:/lhome/rmm/src/ucas-www
start:
	ssh rmm@severn.cs.nott.ac.uk screen -Lmd ${RUN}

deploy: stop mirror start
