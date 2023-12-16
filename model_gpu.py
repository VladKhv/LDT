
import torch
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
from config_telebot import *


class Conversation:
    def __init__(
        self,
        message_template=DEFAULT_MESSAGE_TEMPLATE,
        system_prompt=DEFAULT_SYSTEM_PROMPT,
        response_template=DEFAULT_RESPONSE_TEMPLATE
    ):
        self.message_template = message_template
        self.response_template = response_template
        self.messages = [{
            "role": "system",
            "content": system_prompt
        }]

    def add_user_message(self, message):
        self.messages.append({
            "role": "user",
            "content": message
        })

    def add_bot_message(self, message):
        self.messages.append({
            "role": "bot",
            "content": message
        })

    def get_prompt(self, tokenizer):
        final_text = ""
        for message in self.messages:
            message_text = self.message_template.format(**message)
            final_text += message_text
        final_text += DEFAULT_RESPONSE_TEMPLATE
        return final_text.strip()

class AnswerSearchModel:
    def __init__(self) -> None:
        
        config = PeftConfig.from_pretrained(MODEL_NAME)
        self.model = AutoModelForCausalLM.from_pretrained(
            config.base_model_name_or_path,
            load_in_4bit = True,
            torch_dtype = torch.float16,
            device_map = "auto",
        )
        self.model = PeftModel.from_pretrained(
            self.model,
            MODEL_NAME,
            torch_dtype = torch.float16
        )
        self.model.eval()
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
        self.generation_config = GenerationConfig.from_pretrained(MODEL_NAME)
        print(self.generation_config)
    

    def generate(self, model, tokenizer, prompt, generation_config):
        data = tokenizer(prompt, return_tensors="pt", add_special_tokens=False)
        data = {k: v.to(model.device) for k, v in data.items()}
        output_ids = model.generate(
            **data,
            generation_config = generation_config
        )[0]
        output_ids = output_ids[len(data["input_ids"][0]):]
        output = tokenizer.decode(output_ids, skip_special_tokens = True)
        return output.strip()

    def predict_answer(self, user_message: str) -> str:                       
        conversation = Conversation()
        conversation.add_user_message(user_message)
        prompt = conversation.get_prompt(self.tokenizer)
        output = self.generate(self.model, self.tokenizer, prompt, self.generation_config)            
        return output 
    
model_qa = AnswerSearchModel();
