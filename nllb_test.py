from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "facebook/nllb-200-distilled-600M"

print("Loading model... (first time will download, wait)")

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def translate(text, src_lang, tgt_lang):
    tokenizer.src_lang = src_lang

    inputs = tokenizer(text, return_tensors="pt", padding=True)

    translated_tokens = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.lang_code_to_id[tgt_lang],
        max_length=512
    )

    return tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]

print(translate("નમસ્તે", "guj_Gujr", "eng_Latn"))
