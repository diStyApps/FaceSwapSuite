@echo off

set PYTORCH_CUDA_ALLOC_CONF=garbage_collection_threshold:0.8,max_split_size_mb:512
set CUDA_MODULE_LOADING=LAZY

REM Activate the existing venv
call venv\Scripts\activate.bat

REM Run FaceSwapSuite
python main.py

REM Deactivate the venv
call venv\Scripts\deactivate.bat

pause
