if [ "${PYTHON_VERSION}" == "3.8-dev" ]
then
  choco install python --pre
else
  choco install python --version ${PYTHON_VERSION}
fi
export PATH="/c/python${PYTHON_VERSION:0:1}${PYTHON_VERSION:2:1}/Scripts:/c/python${PYTHON_VERSION:0:1}${PYTHON_VERSION:2:1}:${PATH}"