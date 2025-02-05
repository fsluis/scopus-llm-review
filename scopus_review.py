import os
from llama_cpp import Llama

# https://huggingface.co/bartowski/gemma-2-27b-it-GGUF
llm = Llama(
    model_path=os.path.expanduser("~/models/gemma-2-27b-it-Q6_K_L.gguf"),
    n_gpu_layers = -1,
    n_batch = 512,
    n_ctx=2024 # context window
)

# Load the dataframe
import pandas as pd
df = pd.read_csv(os.path.expanduser("20241121-scopus.csv"))

# Your paper's abstract
my_abstract = "This study examines how information-seeking processes influence socially and ethically responsible consumption. Moving beyond the intention-behavior gap, we highlight the critical role of search behaviors and information barriers in shaping the valuation of secondary ethical aspects during decision-making. Our findings reveal that accessible and transparent information can drive prioritization of responsible aspects, even among consumers with low initial ethical intentions. This work underscores the need for improved information systems and decision-support tools to address barriers and foster responsible consumption."

# Function to construct the prompt
def construct_prompt(title, abstract):
    return f"""I want you to evaluate whether an abstract of a reference paper is relevant to a paper I'm writing. I'll give you details of both my paper and the reference paper. 
    
    My paper:
    Abstract: {my_abstract}
    
    Reference paper:
    Title: {title}
    Abstract: {abstract}
    
    I am particularly interested in knowing whether a paper relates to either of:
    a) Information seeking: Studies of information seeking and sustainable or responsible consumption, including information seeking challenges experienced by consumers;
    b) Information availability: Studies showing the influence of information availability or barriers on responsible or sustainable consumer behavior;
    c) Asymmetries: Studies showing the existence of information asymmetries between market players and consumers, such as through greenwashing practices;
    d) Sustainability: Studies showing the importance of sustainable practices, but are not directly relevant to my study;
    e) Other: There might be other categories of relations. Do feel free to add / interpret new types of relations.
    
    Be critical when estimating relevance. If it is not about sustainability or responsible consumption, it is not relevant.
    
    Does the reference paper seem relevant? If yes, how can it be utilized in my research? Answer in a structured way:
        Relevance: Yes, possibly, no
        Relation: Seeking, availability, asymmetries, sustainability, other 
        Utilization: Explain how this paper can be utilized in my research
    """


def query_llm(prompt):
    response = llm.create_chat_completion(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response


# Test with the first row
first_row = df.iloc[0]
test_prompt = construct_prompt(first_row['Title'], first_row['Abstract'])
test_response = query_llm(test_prompt) # , max_tokens=0
#test_response_text = test_response["choices"][0]["text"]
test_response_text = test_response['choices'][0]['message']['content']
print(test_response_text)


# Function to parse the response and extract relevance, relation, and possible use
def parse_response(response_text):
    # Initialize variables to store the parsed relevance, relation, and possible use
    relevance, relation, possible_use = "No", "", ""
    #
    # Splitting the response into lines and parsing
    lines = response_text.strip().split('\n')
    parsing_utilization = False
    utilization_lines = []
    #
    for line in lines:
        if "**Relevance:**" in line:
            relevance = line.split("**Relevance:**")[1].strip()
            parsing_utilization = False  # Reset when reaching relevance
        elif "**Relation:**" in line:
            relation = line.split("**Relation:**")[1].strip()
        elif "**Utilization:**" in line:
            parsing_utilization = True
            # Start capturing the utilization text from the next line
            utilization_lines = []
        elif parsing_utilization:
            utilization_lines.append(line)  # Append with newline preservation
    #
    # Join all lines captured for utilization to form a complete section
    possible_use = '\n'.join(utilization_lines)  # Use newline for joining
    #
    return relevance, relation, possible_use


test_relevance, test_relation, test_possible_use = parse_response(test_response_text)
print("Test output:")
print("Relevance:", test_relevance)
print("Relation:", test_relation)
print("Possible use:", test_possible_use)

# Wait for user input to continue
input("Press Enter to continue with processing the entire dataframe...")

# Add columns for relevance and possible use
df["Relevance"] = ""
df["Relation"] = ""
df["Possible use"] = ""

# Iterate over the dataframe and apply the function
#for index, row in df.head(10).iterrows():
for index, row in df.iterrows():
    prompt = construct_prompt(row['Title'], row['Abstract'])
    #response = llm(prompt, max_tokens=0)
    response = query_llm(prompt)  # , max_tokens=0
    #response_text = response["choices"][0]["text"]
    response_text = response['choices'][0]['message']['content']
    relevance, relation, possible_use = parse_response(response_text)
    df.at[index, 'Relevance'] = relevance
    df.at[index, 'Relation'] = relation
    df.at[index, 'Possible use'] = possible_use

#df.head(10)[["Relevance","Relation"]]
#df.at[8, "Abstract"]
#df.at[8, "Possible use"]

# Save the updated dataframe
df.to_csv(os.path.expanduser("20241121-scopus-gemma-2-27b-it-Q6_K_L.csv"), index=False)
