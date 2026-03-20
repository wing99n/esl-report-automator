# AI-Powered report tool for teachers

## Overview

Filling out forms and reports manually can be a great pain for many.  
I built this tool to help an english teacher that needs to make student reports for a company every few months. The tool takes in all the inputs it needs
about the student's progress and generates a formatted pdf with all the needed info,
a nice neat table and an ai generated summary of the student's progress
based on the info the user gives it. 

In short, the tool cuts the time it takes to make a report by ~70% (from about
10 minutes down to ~3). This can save the teachers some headache  
and a lot of precious time.

Key features:

* Pdf generation - converts the data into a standardized pdf format

* AI driven summaries - Utilizes Ollama (Llama 3.2) to generate context-aware progress comments based on specific student scores.

* Data Consistency: Uses Pandas to calculate performance averages and ensure table accuracy, eliminating manual calculation errors.

* User-Centric Design: Features a logical, terminal-based workflow that allows for batch reporting without restarting the application.

* HITL checks: Ensures that the data is saved exactly as the user wants it by letting them check. Typo-proof

### Technical stack
Python - Core logic and control flow  
Pandas - Data structuring and calculations  
Ollama - Local LLM integration for text generation  
FPDF2  - Handles the final look and formatting

### Setup
1) Clone the repository:

   git clone https://github.com/wing99n/esl-report-automator.git  
```bash
cd esl-report-automator
 ```
2) Ensure you have python 3.x installed, then run:  
```bash
pip install -r requirements.txt
 ```
3) Set up the specific AI model  

  Download ollama from ollama.com  
  Pull the specific model used in the script   
  ```bash
   ollama pull llama3.2:3b
  ```
4) Run the application  
  ```bash
python main.py
 ```

## Technical deep dive

### How the programme runs

* Initialization - The programme asks the teacher for the data  
they need to fill in for the report. Every step uses HITL validation  
loop to optimize user experience and prevent mistakes in the data. Furthermore,
try-except blocks are used where mistakes could occur (for example the student scores, that 
have to be an integer/float so that the mean could be calculated)

* Data Processing - Pandas is used to make a DataFrame out of the test  
results and calculate an error-proof mean of the student's scores. B

* AI Powered Evaluation - The user has the option to add extra information about the student.
The programme then sends a prompt in the form of an engineered f-string
to ollama and gets a personalised student evaluation

* PDF Generation - The report is generated via FPDF with all the data  
formatted to comply with the company's rules. The pdf is saved to the path the user chooses
with the default being a desktop folder.

Note on the PDF generation:
Localization & Encoding - Integrated custom Unicode font support (ArialCzech) to ensure the correct rendering of Czech diacritics (ě, š, č, ř, ž, ý, á, í, é). 
This ensures the generated reports maintain professional standards for local clients. It also means that the programme may show an error message for the font, however
the code is tested to have run correctly.
* Re-usability -To maximize efficiency, the script features a continuous execution loop.
Users can generate subsequent reports while retaining static metadata (like Client or Language),
drastically cutting down data-entry time for large classes.

### Customisation


* Font Compatibility: The script currently fetches the Arial font from a hardcoded Windows path. 
If you are running this on macOS or Linux, you will need to update the font path 
in the generate_pdf function to point to a valid .ttf file on your system.


* Streamlining Inputs: If you find yourself repeatedly entering the same Klient or Lektor 
for every session, you can hardcode these variables at the top of the main() function to further reduce data-entry time.
On the other hand if your report needs different info in it you can delete or add variables. However this
will add some work to do so that the pdf formats well.


* The prompt: In the main() function you can adjust the prompt to your liking.
Since the prompt is an f-string, you can also plug other data into it.


* Model Performance: While the tool is compatible with many Ollama models, it is optimized for smaller sized models like llama3.2:3b. 
Testing with larger models like Mistral or Qwen resulted in significantly slower generation times (latency).


* API Extensibility: The LLM interaction is strictly isolated within the call_ai() function. While the project defaults to a local 
Ollama instance for data privacy and zero cost, the function can be easily modified to call cloud-based APIs (like OpenAI’s GPT-4o or Google’s Gemini) 
if higher reasoning capabilities or faster cloud-processing are required for larger batches.
  
