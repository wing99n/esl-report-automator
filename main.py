from fpdf import FPDF
import pandas as pd
import ollama
from pathlib import Path
def main():
    '''Uses while loops to fill in all the data about the language course.
    Offers the possibilty to save some of the data for re-use.

    This is also the place to edit the prompt that is sent to ollama'''
    while True:
        klient = get_info_text("Klient")
        obdobi = get_info_text("Období")
        lektor = get_info_text("Lektor")
        jazyk = get_info_text("Jazyk")
        while True:
            kurz = get_info_text("Kurz")
            vyuka = get_info_text("Výuka")
            vyhodnoceni_df = get_test_data()
            student = vyhodnoceni_df.loc[0, 'Student']
            more_info_on_student = get_info_text("More info on student")
            prompt = f"""
            Role: You are a professional English as a Second Language (ESL) instructor.
            Task: Write a ~ 50 word progress report for a student {student}.
            Student progress info: {more_info_on_student}
            
            Constraints:
            1. The tone must be professional and motivating.
            2. The report must be exactly 4 sentences long.
            3. Focus on specific improvements mentioned in the provided data. If the input notes are brief or informal, expand on them logically using standard academic ESL terminology.
            4. Use clear, academic English.
            5. Dont use phrases like here's your report: just write the report as if it were a field in a form
            6. The class is a 1 on 1 lesson with just the student and the teacher"""
            while True:
                response = call_ai(prompt)
                print(f'Here is the AI student evaluation: {response}')
                satisfaction = yes_or_no('Do you want to use the student evaluation above?')
                if satisfaction:
                    break
                else:
                    print('New evaluation is being generated...')
                    continue
            generate_pdf(klient, obdobi, kurz, jazyk, lektor, vyuka, vyhodnoceni_df, response, student)
            print(f"Your {student} report for {klient} has been generated.")

            another_report = yes_or_no("Do you want to make another report (y/n)?")
            if another_report:
                pass
            else:
                return 'Done'
            set_data_again = yes_or_no(
                "Do you want to reset the data for the less changed values \n (klient, období, lektor or jazyk?) for another report (y/n) ")
            if set_data_again:
                break
            else:
                continue


def get_info_text(value):
    '''This function serves as the primary data-getter for the answers you want as a string
     such as the client name. It also has a HITL verification added

     Args: The type of data you want to get from the user as a string. For example:
     value = 'Teacher name'
     would mean that the user would see an input asking: "Please enter Teacher name:"
     For the specific needs of report style,
     there is a requirement for the user input to be at least 2 words if you put in student as an arg so that you get
     both the name and the surname.

     Returns: Anything that the user writes in and confirms as the input as a string'''
    original_value = value
    while True:
        value = input(f"Please enter {original_value}: ").strip()
        if original_value.lower() == "student":
            name_and_surname = value.split(" ")
            if len(name_and_surname) >= 2:
                pass
            else:
                print("Please enter the student's name and surname")
                continue

        if value:
            confirmation = input(f"Do you want it saved as: {value}? (y/n): ").lower().strip()
            if confirmation in ['y', 'yes', 'si', 'ok']:
                break
            else:
                continue
        else:
            print(f"Please enter {original_value}.")
            continue
    return value
def get_info_int(value):
    '''Retrieves a number (a test score from 0-100) as a float

    Args: The subject you want the test score of as a string

    Returns: A number as a float'''
    original_value = value
    while True:
        value = input(f"Please enter {original_value}: ").strip()
        try:
            float_value = float(value)
            if float_value < 0 or float_value > 100:
                raise ValueError
        except ValueError:
            print(f"Please enter {original_value} as a score from 0 to 100.")
            continue

        confirmation = input(f"Do you want it saved as: {value}? (y/n): ").lower().strip()
        if confirmation in ['y', 'yes', 'si', 'ok']:
            break
        else:
            continue
    return float_value
def get_english_levels():
    '''Retrieves the entry and exit level of the student's english.
    The user input must include one of the CEFR English levels (A1 - C2)

    Returns: a tuple of the entry and exit level of the student's English in this order both as strings'''
    while True:
        vstupni_uroven = input("Vstupní úroveň aj: ").strip()
        if any(level in vstupni_uroven.lower() for level in ['a1', 'a2', 'b1', 'b2', 'c1', 'c2']):
            confirmation = input(f"Do you want it saved as: {vstupni_uroven}? (y/n): ").lower().strip()
            if confirmation in ['y', 'yes', 'si', 'ok']:
                break
            else:
                continue
        else:
            print(f"Please enter a specific english level (a1-c2).")
            continue

    while True:
        vystupni_uroven = input("Výstupní úroveň aj: ").strip()
        if any(level in vystupni_uroven.lower() for level in ['a1', 'a2', 'b1', 'b2', 'c1', 'c2']):
            confirmation = input(f"Do you want it saved as: {vystupni_uroven}? (y/n): ").lower().strip()
            if confirmation in ['y', 'yes', 'si', 'ok']:
                break
            else:
                continue
        else:
            print(f"Please enter a specific English level (A1-C2).")
            continue
    return vstupni_uroven, vystupni_uroven
def get_test_data():
    '''Uses the get_info_text(), get_info_int() and get_english_levels()functions to retrieve the test data
    and puts them into a pandas dataframe

    Returns: a pandas dataframe with the test scores, the student's full name and the entry and exit
    English levels'''
    student = get_info_text("Student")
    vstupni_uroven, vystupni_uroven = get_english_levels()
    use_of_english_score = get_info_int("Use of English Score")
    speaking_score = get_info_int("Speaking Score")
    writing_score = get_info_int("Writing Score")
    listening_score = get_info_int("Listening Score")
    reading_score = get_info_int("Reading Score")
    scores = pd.Series([use_of_english_score, speaking_score, writing_score,
                        listening_score, reading_score])

    vyhodnoceni_df = pd.DataFrame({"Student": [student],
                                   "Vstupní úroveň": [vstupni_uroven],
                                   "Dosažená úroveň" : [vystupni_uroven],
                                   "Vyhodnocení testů (%)": [scores.mean().round(1)],
                                   "Použití jazyka\n(%)": [use_of_english_score],
                                   "Mluvení(%)" : [speaking_score],
                                   "Psaní(%)":[writing_score],
                                   "Poslech(%)": [listening_score],
                                   "Čtení(%)" : [reading_score]})
    return vyhodnoceni_df
def call_ai(prompt):
    '''Writes a student evaluation based on the collected data and the prompt in the
    main() function using the ollama library to communicate with a local LLM

    Args: a f-string prompt about the student from the main() function

    Returns: an AI generated student evaluation as a string'''
    client = ollama.Client()
    model = "llama3.2:3b"
    prompt = prompt.strip()
    response = client.generate(model = model, prompt = prompt)
    return response.response
def generate_pdf(klient, obdobi, kurz, jazyk, lektor, vyuka, vyhodnoceni_df, response, student):
    '''Generates a formatted PDF based to all the data collected

     Args: a lot of them, depending on all the data you want in the final pdf
     In this case the client name,period, course name, language, teacher name, time of classes as strings,
      the dataframe made in get_test_data(), and the AI response and student name both as strings

      Returns: a PDF stored in a local folder'''
    home = Path.home()
    if (home / "OneDrive" / "Desktop").exists():
        desktop_path = home / "OneDrive" / "Desktop" / "hodnoceni_studentu"
    else:
        desktop_path = home / "Desktop" / "hodnoceni_studentu"
    desktop_path.mkdir(parents=True, exist_ok=True)
    file_path_and_name = desktop_path / f"{student}_{obdobi}.pdf"
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", style = "B", size = 20)
            self.set_x(90)
            self.cell(30, 10, "Hodnocení", align="C")

    pdf = PDF('P', 'mm', 'A4')
    pdf.add_font("ArialCzech", "", r"C:\Windows\Fonts\arial.ttf")
    pdf.add_font("ArialCzech", "B", r"C:\Windows\Fonts\arialbd.ttf")
    pdf.set_left_margin(15)
    pdf.set_right_margin(15)
    pdf.add_page()
    pdf.set_y( 30)
    pdf.set_font("ArialCzech", size = 12)
    pdf.cell(0, 10, f"Klient: {klient}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, f"Období: {obdobi}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, f"Kurz: {kurz}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, f"Lektor: {lektor}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, f"Jazyk: {jazyk}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, f"Výuka: {vyuka}", new_x="LMARGIN", new_y="NEXT")
    headers = vyhodnoceni_df.columns.tolist()
    data_rows = vyhodnoceni_df.values.tolist()
    full_table_date = [headers] + data_rows
    pdf.ln(10)
    pdf.set_font("ArialCzech", size=11)
    col_widths = (3, 3, 3, 4, 2.5, 2.5, 3, 2.5, 3)
    with pdf.table(col_widths=col_widths, text_align="CENTER", line_height=9) as table:
        for data_row in full_table_date:
            row = table.row()
            for value in data_row:
                row.cell(str(value))
    pdf.ln(10)
    pdf.set_font("ArialCzech", size=14)

    pdf.cell(0, 10, f"Komentář", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("ArialCzech", size=12)
    pdf.cell(0, 10, f"{student}", new_x="LMARGIN", new_y="NEXT")
    pdf.multi_cell(0, 10, text=str(response))
    pdf.output(file_path_and_name)

def yes_or_no(question):
    '''A helper function to get a simple yes/no answer

    Args: the question you want to ask as a string

    Returns: True for yes and False for no'''
    while True:
        again = input(f"{question}  ").lower().strip()
        if again == "y" or again == "yes":
            return True
        elif again == "n" or again == "no":
            return False
        else:
            print("Please enter yes or no (y/n).")



if __name__ == "__main__":
    main()