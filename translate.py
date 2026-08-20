from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "facebook/nllb-200-distilled-600M"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def translate_text(text, src_lang, tgt_lang):
    tokenizer.src_lang = src_lang

    inputs = tokenizer(text, return_tensors="pt")
    tokens = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.convert_tokens_to_ids(tgt_lang),
        max_length=512
    )

    return tokenizer.batch_decode(tokens, skip_special_tokens=True)[0]
