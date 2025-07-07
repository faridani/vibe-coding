# A Guide to Vibe-Coding Large Projects 

I tried to come up with a guide for vibe-coding large greenfield projects. Here's my suggestion—wondering what else we should add to this list:

## 0- You do not need to pay for an IDE

Tools like Cursor, Windsurf, or Lovable are great for iterative improvements but less ideal for starting large greenfield projects from scratch. In my experience, these are too overfitted to a small niche audience. As for an IDE, I used to use IntelliJ and PyCharm, but I use VSCode for everything now.

## 1- You DO NEED to pay for a top-tier LLM subscription

Subscribe to premium foundation models. They're invaluable for brainstorming and refining complex project decisions. I pay for Gemini Pro, ChatGPT Pro, and SuperGrok. Claude is smart but unfortunately does not have a good UI to handle large codebases and constantly hits token limits.

## 2- Brainstorm architecture with AI

Gemini Pro, in my opinion, is the best at architecture. Use Gemini Pro to explore architecture and infrastructure options. Ask it to stick to a single ecosystem (e.g., GCP, AWS, Azure) for simplicity and scalability rather than custom infrastructure, which can become unwieldy.

## 3- Validate with multiple AI perspectives

After you've used Gemini Pro to come up with the first draft, run your design through ChatGPT and Grok to catch blind spots or innovative additions. Prioritize simplicity and modularity in your architecture to ensure flexibility for future expansion.

## 4- Use Gemini Pro to write your code and ChatGPT/Grok to perform code review

Pick a primary coder (I use Gemini Pro) and use the others as code reviewers (I use ChatGPT and Grok for review). When your reviewers catch errors, ask your primary coder to fix them. In my experience, reviewers add too many errors if you ask them to find bugs and correct them simultaneously.

## 5- Erase your context window frequently and don't let it get cluttered with noise

In my experience, Gemini Pro usually fixes my bugs if I dump my latest files into a fresh chat window rather than keeping a very long multi-day chat session going. It's probably more energy efficient too.

## 6- For graphics and icons, just use Sora

Gemini Pro and Grok do not do a good job with icons.

## 7- Use Git like your life depends on it

Otherwise, you will waste your time. Commit only stable, working versions. Stage changes frequently (aka `git add .`) and use `git restore .` liberally to revert broken states. Maintain clean commits and use tags. Your main branch should always be the best polished version that is just a few commits behind your staged changes.

## 8- Use containers and environments religiously

Use Dockerfiles, requirements.txt, and config files to manage dependencies and environments.

## 9- Build a robust testing framework

This is a must. These AI coding tools are not perfect. Integrate testing early. Use unit tests, integration tests, and CI/CD pipelines to ensure you're incrementally improving without breaking existing functionality. Keep an eye on any new warnings or errors in the console.

## 10 - Build your own tooling to feed code to generic AI tools

I have found that the Unix tree command is a very effective way to send my folder structure to these tools. I just paste my files and the output of the tree command to the AI. I also diff the AI output with what I have to make sure the AI isn't touching code blocks that it's not supposed to touch.

* see [tree.md](lessons/tree.md) for more on trees
* see [diff.md](lessons/diff.md) for more on diffing two files 

## 11- Introduce features gradually

Use an agile board (e.g., Jira, Trello) to prioritize tasks. Roll out features methodically, testing thoroughly to maintain stability and avoid technical debt.

## 12- Use your technically trained brain to lead the AI, but don't force it

I have noticed I should not force the AI to use my preferred tool, or it might do it poorly. In my experience, it's better to say "Compare Cloudflare with Firebase and help me choose the right deployment tool" rather than just forcing the AI to use the one that you like, which might very well be inferior and outdated.

## 13- Leverage modern deployment

Adopt platforms like Cloudflare for seamless deployments. Avoid outdated methods like SFTP, which are slow and error-prone.

## 14- DO NOT TRUST THE AI WITH SECURITY ROLES

If you ask an AI like Gemini Pro to suggest roles for your system accounts, it starts to liberally give them admin access, opening huge security holes in your system. It's best to double-check any suggestion against the official latest documentation, as these AI tools often latch onto outdated documentation or Stack Overflow posts that are problem-riddled.

## 15- And lastly, make sure you enjoy the ride

Document as you go, feed your logs continuously to your AI for insights. Do not assume AI is magically going to solve everything. Read its answers fully, do not lose sight of what you eventually need to ship, and play nice music in the background to enjoy the ride. Also let me know your own tips for vibe-coding large projects
