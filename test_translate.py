from translate import translate_text

text = "Technology is very important in daily life."

print("Hindi:")
print(translate_text(text, "eng_Latn", "hin_Deva"))

print("Gujarati:")
print(translate_text(text, "eng_Latn", "guj_Gujr"))
