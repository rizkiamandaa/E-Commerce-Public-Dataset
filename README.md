{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "f39c796e-d8c0-4b84-a73f-00cbb9388ec8",
   "metadata": {},
   "source": [
    "# Dicoding Collection Dashboard"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "126ead31-1d04-46d4-b930-ad630f478e09",
   "metadata": {},
   "source": [
    "## Setup Environment - Anaconda"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "c6b90122-a1e8-4ab2-885f-ccb0e9c21a44",
   "metadata": {},
   "source": [
    "conda create --name main-ds python=3.10.2\n",
    "\n",
    "conda activate main-d\n",
    "\r\n",
    "pip install -r requirements.txt"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "a2a52cc0-a4f9-481a-9637-bc87106dad9c",
   "metadata": {},
   "source": [
    "## Setup Environment - Shell/Terminal"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "1ab1d185-e963-4468-ad24-273b2b051c5c",
   "metadata": {},
   "source": [
    "mkdir proyek_analisis_data\n",
    "cd proyek_analisis_data\n",
    "pipenv install\n",
    "pipenv shell\n",
    "pip install -r requirements.txt"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "b6d5fe1b-3774-4d84-9062-2afe7f192ff5",
   "metadata": {},
   "source": [
    "## Run Streamlit App"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "b417afc0-b968-4d24-9046-939054cf6fd2",
   "metadata": {},
   "source": [
    "streamlit run Dashboard.py"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.2"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
