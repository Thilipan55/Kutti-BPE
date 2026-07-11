# Kutti-BPE
---
Download from:
```bash
!git clone https://github.com/Thilipan55/Kutti-BPE.git
```


There are 256 “foundational tokens” which are just vocab[i] = bytes(i) so the BPE training loop to make the dictionary looped the dataset over and minted 4500 new tokens so adding with foundation tokens of 256 → 4756

Well, Encoding and training Tamil is way different that encoding latin languages like english since they are far down the unicode table. English are standard ASCII so to represent ‘a’ its just bytes[97]  so just one token we can merge this to make many common words like ‘and’ which is 3 tokens, ‘apple’ which is 5 tokens and 5 bytes.

But tamil, is way down the table and for example, த → 3 bytes → E0 AE A4 (Hex), So unlike english to represent one letter we need 3 bytes, so we are spending more time in just these merges to make one token, And even worse சி these syllable letters takes ச → 3 bytes and ி → 3 bytes

so to make சி it needs as many merges to make 1 letter and as many merges i like to call them “scafolding” tokens to build that one which most of the time we wont use in most of the other vocab to build other tokens

I will expand and structure this such that all devs can use it in the future. :)
