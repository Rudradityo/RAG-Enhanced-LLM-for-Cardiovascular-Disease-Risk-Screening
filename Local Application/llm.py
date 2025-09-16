from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

# Specify Device
device = torch.device('cpu')

# Specify path to fine-tuned T5 in your local
model_path = "./finetuning/final_version/fine_tuned"

# Load the tokenizer
tokenizer = T5Tokenizer.from_pretrained(model_path)

# Load the model
model = T5ForConditionalGeneration.from_pretrained(model_path).to(device)

# Set model to evaluation mode
model.eval()


# Generate Prediction on Prompt
def process_prompt(prompt):

    print(f"Prompt in llm.py:\n{prompt}\n")
    
    # Tokenize prompt
    tokenized_query = tokenizer(prompt, max_length=512, truncation=True, padding='max_length', return_tensors='pt')
    
    print(f"Tokenized Prompt in llm.py:\n{tokenized_query}\n")

    # Move tensors to device
    input_ids = tokenized_query['input_ids'].to(device)
    attention_mask = tokenized_query['attention_mask'].to(device)

    with torch.no_grad():  # Disable gradient calculations during inference
        outputs = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_length=150,  # Adjust the maximum length of the generated output
            num_beams=4,  # For beam search (improves quality but is slower)
            early_stopping=True,
        )

    print(f"Outputs in llm.py:\n{outputs}\n")

    decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print(f"Decoded Output in llm.py:\n{decoded_output}\n")

    return decoded_output
    
#def main():
    
    
#if __name__ == "__main__":
#    main()