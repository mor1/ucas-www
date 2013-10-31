# Copyright (c) 2012, Richard Mortier <mort@cantab.net>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

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
