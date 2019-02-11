choco install python --version ${PYTHON_VERSION}
export PATH="/c/python${PYTHON_VERSION:0:1}${PYTHON_VERSION:2:1}/Scripts:/c/python${PYTHON_VERSION:0:1}${PYTHON_VERSION:2:1}:${PATH}"
