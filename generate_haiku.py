import os
from transformers import GPT2LMHeadModel, GPT2Tokenizer
#import torch  # Make sure you import torch for tensor operations




# Load the model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")


# Add pad_token if not already set
if tokenizer.pad_token is None:
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    model.resize_token_embeddings(len(tokenizer))  # Update model embedding size

print(f"Pad token set to: {tokenizer.pad_token}, ID: {tokenizer.pad_token_id}")

# Function to count syllables in a line (a simple approximation)
def count_syllables(line):
    vowels = "aeiouy"
    line = line.lower().strip()
    count = 0
    prev_char = ""
    for char in line:
        if char in vowels and (prev_char not in vowels):
            count += 1
        prev_char = char

    if line.endswith("e"):
        count -= 1
    if count == 0:
        count = 1
    return count

# Function to generate a full haiku based on the user's prompt
# In generate_haiku.py



def generate_full_haiku(prompt):
   
    # Step 1: Print the received prompt
    print("Debug: Received Prompt ->", prompt)

    # Define the padding token if not already set
    #if tokenizer.pad_token is None:
        #tokenizer.add_special_tokens({'pad_token': tokenizer.eos_token})

 # Tokenize the prompt
    input_ids = tokenizer.encode(prompt, return_tensors="pt")

     # Step 2: Print the tokenized input
    print("Debug: Tokenized Input IDs ->", input_ids)

    # Ensure the prompt explicitly requests a haiku
    if not prompt.lower().startswith(""):
        prompt = f"Write a 5-7-5 syllable following haiku about {prompt}."


   

    # Create an attention mask
    attention_mask = input_ids != tokenizer.pad_token_id

    # Generate text
    output = model.generate(
        input_ids,
        attention_mask=attention_mask,
        #min_length=15,
        max_length=100,  # Adjusted for haiku and additional context
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        do_sample=True,
        top_k=50,
        top_p=0.85,
        temperature=0.7, 
        pad_token_id=tokenizer.pad_token_id 
    )

    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    # Remove the prompt from the generated text
    if generated_text.lower().startswith(prompt.lower()):
        generated_text = generated_text[len(prompt):].strip()

    # Step 3: Print the raw generated text
    print("Debug: Generated Text (Raw) ->", generated_text)


    # Save the generated text to a file
    file_path = os.path.join(os.path.dirname(__file__), "gen_text.txt")
    try:
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(f"Prompt: {prompt}\n")
            file.write("Generated Text:\n")
            file.write(generated_text + "\n\n")
    except Exception as e:
        print(f"Error writing to file: {e}")

    # Split the generated text into lines
    lines = generated_text.split("\n")
    haiku = []
    syllable_pattern = [5, 7, 5]  # Haiku syllable structure

    for line in lines:
        syllables = count_syllables(line.strip())
        print(f"Debug: Line '{line.strip()}' has {syllables} syllables")  # Debug syllable count
        if syllables in syllable_pattern:
            haiku.append(line.strip())
            syllable_pattern.pop(0)
        if not syllable_pattern:
            break

    # Save haiku separately if it matches the 5-7-5 structure
    if len(haiku) == 3:
        print("Debug: Successfully created a Haiku ->", "\n".join(haiku))

        try:
            with open(file_path, "a", encoding="utf-8") as file:
                file.write("Generated Haiku:\n")
                file.write("\n".join(haiku) + "\n\n")
        except Exception as e:
            print(f"Error writing haiku to file: {e}")

    else:
        print("Debug: Failed to create a valid Haiku")
        return "Could not generate a valid haiku. Try again!"
    # Return the haiku to display in the GUI
    return "\n".join(haiku)

    # If no haiku is generated, return the full text instead of an error
    #return generated_text



