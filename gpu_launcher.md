# GPU Launcher

This document provides instructions for running the video generation script on different platforms with GPU support.

## Kaggle

1.  Go to: https://www.kaggle.com
2.  Create New → Notebook
3.  In the right-hand menu, under "Settings", select "GPU" as the accelerator.
4.  Upload your `gpu_fallback.py` script and any other necessary files.
5.  Run your script in a notebook cell:

    ```python
    !python your_script_name.py
    ```

## Google Colab

1.  Go to: https://colab.research.google.com
2.  Create a new notebook.
3.  Go to "Runtime" → "Change runtime type".
4.  Select "GPU" from the "Hardware accelerator" dropdown menu.
5.  Upload your `gpu_fallback.py` script and any other necessary files to the Colab environment.
6.  Run your script in a code cell:

    ```python
    !python your_script_name.py
    ```

## Hugging Face Spaces

1.  Go to: https://huggingface.co/spaces
2.  Click on "Create new Space".
3.  Choose a Space SDK (e.g., Gradio or Streamlit).
4.  In the "Hardware" settings, select a GPU instance.
5.  Upload your scripts to the Space repository.
6.  Your application will automatically run with GPU support.
