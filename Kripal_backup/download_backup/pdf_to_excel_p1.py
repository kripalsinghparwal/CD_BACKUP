#import libraries 
import fitz  
import pandas as pd
import re

# convert PDF into Dataframe 
def parse_questions_from_pdf(pdf_file):
    '''
    This function helps converting the input PDF into a dataframe and can use it accordingly
    arguments: pdf_file : Provide the path to your PDF file 
    output: Returns a dataframes with 2 columns - Questions and Choices
    '''
    doc = fitz.open(pdf_file)
    questions = []
    current_question = None
    current_choices = []
    inside_question = False

    for page in doc:
        text = page.get_text()
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        for line in lines:
            if re.match(r'^(Q\.|Question|^\d+\.)', line):  # different question formats
                if current_question is not None:
                    questions.append({
                        'question': current_question,
                        'choices': current_choices
                    })
                current_question = line
                current_choices = []
                inside_question = True
            elif re.match(r'(\(\w\)|^\w\.)', line) and inside_question:  #  choice formats
                current_choices.append(line)
            elif inside_question:
                current_question += ' ' + line
            else:
                continue

    if current_question is not None:
        questions.append({
            'question': current_question,
            'choices': current_choices
        })

    doc.close()
    return pd.DataFrame(questions)

# Distribute the choices 
def distribute_options(df):
    '''
    Function todistribute the choices column into different choices 
    '''
    def parse_choices(choices):
        choice_columns = {}
        for i, choice in enumerate(choices):
            choice_label = re.match(r'(\(\w\)|^\w\.)', choice).group(0)
            choice_text = choice[len(choice_label):].strip()
            choice_columns[f'choice_{i+1}'] = f"{choice_label} {choice_text}"
        return choice_columns

    # Apply parse_choices to each row in df['choices']
    df_choices = df['choices'].apply(parse_choices)
    df_choices = pd.DataFrame(df_choices.tolist(), index=df.index)

    # Concatenate original DataFrame with parsed choices
    df = pd.concat([df[['question']], df_choices], axis=1)
    return df

# Main function 
def pdf_to_excel(pdf_file, excel_file):
    df = parse_questions_from_pdf(pdf_file)
    df = distribute_options(df)
    df.to_excel(excel_file, index=False)


pdf_file = 'PDFs/type_2.pdf'  
excel_file = 'output.xlsx'  
pdf_to_excel(pdf_file, excel_file) #final_function