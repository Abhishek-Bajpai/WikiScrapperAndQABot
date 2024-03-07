import torch
from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering, TrainingArguments, Trainer
from sklearn.model_selection import train_test_split

def load_data_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.readlines()
    except Exception as e:
        print(f"Error loading data from file: {e}")
        return None

    dataset = []
    for line in data:
        parts = line.strip().split('\t')
        if len(parts) >= 2:
            question, context = parts[0], '\t'.join(parts[1:])
            dataset.append({'question': question, 'context': context})
        else:
            print(f"Ignoring invalid line: {line}")
    return dataset if dataset else None

def main():
    file_path = 'linked_articles_content.txt'
    dataset = load_data_from_file(file_path)
    if dataset is None:
        print("No valid data found. Exiting.")
        return

    train_data, test_data = train_test_split(dataset, test_size=0.2, random_state=42)

    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    model = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-uncased')

    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir='./logs',
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_data,
        eval_dataset=test_data,
        tokenizer=tokenizer,
    )

    trainer.train()
    # Save the fine-tuned model
    trainer.save_model("trained_model/fine_tuned_model")


if __name__ == "__main__":
    main()

