prepenv:
	@echo "*** Creating Virtual Environment ***"
	( \
		python3 -m venv venv_rbac; \
		source venv_rbac/bin/activate; \
		pip install --upgrade pip; \
		pip install -r requirements.txt; \
)

start:
	@echo "*** VIRL Up RBAC Demo ***"
	virl up

nodes:
	@echo "*** Exporting virl nodes IP Addresses ***"
	virl nodes > nodes.txt
	atom ../

cleanup:
	virl down
	rm nodes.txt
