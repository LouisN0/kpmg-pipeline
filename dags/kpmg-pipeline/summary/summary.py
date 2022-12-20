import openai
import os

"""
    Python code to query openai chatGPT and summarize a .txt file
"""

# TODO insert openai key here
chatGPT_api_key = "insert openai key here"
# Set the API key
openai.api_key = chatGPT_api_key

# Set the directory to read the .txt files from
path = "insert path to directory with files"

# initialize empty json to be populated with summarys
cla_summary_json = {}

# define function that summarizes one long file and adds
# it to the cla_summary_json.
# because chatGPT accepts only a limited number of tokens,
# longer documents need to be split into chuncks
def get_summary_long_file(filename):

    with open (filename, "rb") as f:
        text_from_file = f.read()

    text_to_summarize = str(text_from_file)

    # Set the model to use
    model_engine = "text-davinci-003"

    # Set the maximum context length (in tokens) allowed by the model
    max_context_length = 2048

    # Split the text into chunks of the maximum allowed context length
    text = text_to_summarize
    text_chunks = [text[i:i+max_context_length] for i in range(0, len(text), max_context_length)]

    # Send each chunk of text to the model and store the results
    results = []
    for chunk in text_chunks:
        response = openai.Completion.create(
            engine=model_engine,
            prompt=chunk,
            max_tokens=1024,
            temperature=0.5,
        )
        results.append(response["choices"][0]["text"])

    # Concatenate the results into a single string
    result_text = "".join(results)

    # Prompt
    prompt = f"Résume ce document en français: {result_text}"

    # Use the model to generate a summary of the text
    summary_response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5,
    )

    summary = summary_response["choices"][0]["text"]

    cla_summary_json[filename] = summary

# function that loops through files in
# the directory, calls get_summary_long_file()
for file in os.listdir():

    if file.endswith(".txt"):
        try:
            get_summary_long_file(file)
            print(file)
        except:
            print(f"This row throws and error: {file}")

