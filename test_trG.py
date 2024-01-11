from deep_translator import GoogleTranslator
translated = GoogleTranslator(source='russian', target='english').translate('Досымханова Акмарал')
translator= GoogleTranslator(source='russian', target='english')
eng_tr = translator.translate('Досымханова Акмарал')

print(eng_tr)
print('END TRANSLATION')