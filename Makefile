spec:
	spec spec/ -f specdoc --color

features:
	cucumber features/*.feature

staging:
	TARGET=staging cucumber features/app.feature:3

# start the proxy frontend
run-proxy:
	@python aimpl_proxy/aimpl/run.py &
	@echo "proxy started"

# stop the proxy frontend
stop-proxy:
	@bin/stop.sh proxy
	@echo "proxy stopped"

.PHONY: spec features staging run-dummy run-proxy stop-dummy stop-proxy
