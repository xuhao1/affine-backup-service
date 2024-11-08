install:
	@echo "Installing Affine backup service..."
	@chmod +x deploy_service.sh
	@./deploy_service.sh
	@echo "Installation completed."

uninstall:
	@echo "Uninstalling Affine backup service..."
	@chmod +x uninstall_service.sh
	@./uninstall_service.sh
	@echo "Uninstallation completed."
