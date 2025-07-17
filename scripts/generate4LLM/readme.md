**TL;DR:** Script to generate a markdown file with folder structure and file contents for LLM analysis.

This tools is designed to be a low overhead tool. You just add the `dev-tools` directory to the root of your git. And it can generate your folder structure and file contents that you can later use to add context to Gemini/ChatGPT/Claud/Grok etc.

Run the tool from your root directory 

```
Usage: python dev-tools/generate4LLM.py
```

It will run an place a 4LLM.md markdown file in your dev-tools folder. 

We recommend addint the following line to your `.gitignore` 

```bash
4LLM.md* 
```
