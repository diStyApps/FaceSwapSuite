@echo off

REM 1. Create a venv folder
echo Creating venv folder...
python -m venv venv

REM 2. Activate the venv
echo Activating venv...
call venv\Scripts\activate.bat

REM 3. Install dependencies from cuda_requirements.txt
echo Installing dependencies from cuda_requirements
pip install -r requirements\cuda_requirements.txt

REM 4. Install dependencies from roop_requirements.txt
echo Installing dependencies from roop_requirements
pip install -r requirements\roop_requirements.txt

REM 5. Install dependencies FaceSwapSuite from fss_requirements
echo Installing dependencies from fss_requirements.txt
pip install -r requirements\fss_requirements.txt

REM 6. Download inswapper_128.onnx only if it doesn't exist
echo Checking for inswapper_128.onnx...
if not exist "inswapper_128.onnx" (
    echo Downloading inswapper_128.onnx...
    curl -L -o inswapper_128.onnx https://huggingface.co/deepinsight/inswapper/resolve/main/inswapper_128.onnx
) else (
    echo inswapper_128.onnx already exists, skipping download.
)

REM 7. Run FaceSwapSuite
echo Launching FaceSwapSuite
python main.py

pause
