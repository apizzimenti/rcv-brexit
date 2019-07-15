
setup:
	@echo "Creating necessary directories."
	mkdir data
	@echo "Installing requirements."
	git clone https://github.com/apizzimenti/Ranked.git
	@echo "Navigate to the Ranked directory and run python setup.py develop\nto complete the installation."
