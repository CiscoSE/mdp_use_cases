dev: netsim nso sync-from netsim-show

test: nso virl sync-from virl-show 

clean: nso-clean netsim-clean virl-clean

netsim:
	-@ncs-netsim --dir netsim create-device cisco-nx spine1
	-@ncs-netsim --dir netsim add-device cisco-nx spine2
	-@ncs-netsim --dir netsim add-device cisco-nx leaf1
	-@ncs-netsim --dir netsim add-device cisco-nx leaf2
	-@ncs-netsim --dir netsim add-device cisco-nx leaf3
	-@ncs-netsim --dir netsim add-device cisco-nx leaf4
	-@ncs-netsim start

netsim-clean:
	-@ncs-netsim stop
	-@rm -Rf netsim/
	-@rm README.netsim

netsim-show: 
	-@echo "Here are your netsim node status.\n"
	-@ncs-netsim list
	-@echo "\n\n"
	-@echo "Here is the device inventory in NSO.\n"
	-@echo "show devices list" | ncs_cli -C -u admin
	-@echo "\n"

virl: 
	-@virl up --provision
	-@NSO_HOST=localhost NSO_USERNAME=admin NSO_PASSWORD=admin virl generate nso 

virl-show: 
	-@echo "Here are your VIRL node status.\n"
	-@virl nodes
	-@echo "\n\n"
	-@echo "Here is the device inventory in NSO.\n"
	-@echo "show devices list" | ncs_cli -C -u admin
	-@echo "\n"

virl-clean: 
	-@virl down 
	-@rm -Rf .virl

nso:
	#-ncs-setup --dest . --package cisco-nx --package $NCS_DIR/examples.ncs/service-provider/virtual-mpls-vpn/packages/resource-manager
	-@ncs-setup --dest . --package cisco-nx \
	  --package demo_resources/vxlan-evpn \
	  --package demo_resources/resource-manager 
	-@ncs
	-@ncs_load -lm demo_resources/prompt_config.xml

nso-clean:
	-@ncs --stop
	-@rm -Rf README.ncs logs/ ncs-cdb/ ncs-java-vm.log ncs-python-vm.log ncs.conf packages/ state/ storedstate target/ scripts/

sync-from:
	-@curl -X POST -u admin:admin http://localhost:8080/api/running/devices/_operations/sync-from

