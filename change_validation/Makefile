#Makefile

prepenv:
	@echo "*** Creating Virtual Environment ***"
	( \
		python3 -m venv venv_chg; \
		source venv_chg/bin/activate; \
		pip install --upgrade pip; \
		pip install -r requirements.txt; \
		pip install genie.libs.parser --upgrade --pre; \
)

start:
	@echo "*** VIRL Up Change Demo ***"
	virl up
	mkdir tests
	@echo "*** VIRL Up Change Demo ***"
	@echo ""
	@echo ""
	@echo "*** DO NOT FORGET TO SOURCE PYATS DETAILS ***"
	@echo ""
	@echo ""
	@echo "*** DO NOT FORGET TO SET CORE2 IP ADDRESS ***"
	@echo ""
	@echo ""


nodes:
	@echo "*** Exporting virl nodes IP Addresses ***"
	virl generate pyats
	virl nodes > nodes.txt
	atom ../

cleanup:
	virl down
	rm -rf tests
	rm default_testbed.yaml
	rm nodes.txt
