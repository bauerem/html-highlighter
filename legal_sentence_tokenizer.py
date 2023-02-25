from transformers import RobertaTokenizerFast, RobertaForTokenClassification
import torch
import timeit

model_name_or_path = "roberta_sentence_tokenizer"
tokenizer = RobertaTokenizerFast.from_pretrained(model_name_or_path)
model = RobertaForTokenClassification.from_pretrained(model_name_or_path)

def sentence_tokenize(text, batch_size = 6):
	# tokenize
	token_ids = tokenizer.encode(text, return_tensors="pt", add_special_tokens=False, pad_to_multiple_of=254, padding=True)
	# reshape into batches
	token_ids = token_ids.reshape(-1, 254)

	cls_token = torch.tensor([tokenizer.cls_token_id])
	sep_token = torch.tensor([tokenizer.sep_token_id])


	out_ids, out_labels = [], []
	for batch in token_ids:
		input_ids = torch.cat((cls_token, batch, sep_token))
		logits = model(input_ids.unsqueeze(dim=0)).logits #.detach().cpu()
		labels = logits[0][1:-1].argmax(dim=1).detach().cpu().tolist()
		out_labels.extend(labels)
		out_ids.extend(input_ids[1:-1].detach().cpu().tolist())


	result = []
	sent = []
	for w, pred in zip(out_ids, out_labels):
		# padding token
		if w == 1:
			continue
		sent.append(w)
		if pred == 1:
			result.append(tokenizer.decode(sent))
			sent = []
	return result
