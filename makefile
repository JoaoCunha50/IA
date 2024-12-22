# Nome do interpretador Python
PYTHON = python3

# Arquivo principal
MAIN = src/main.py

# Target padrão
run:
	$(PYTHON) $(MAIN)

# Limpeza de arquivos desnecessários
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -r {} +

# Instalar dependências (caso exista um requirements.txt)
install:
	pip install -r requirements.txt
