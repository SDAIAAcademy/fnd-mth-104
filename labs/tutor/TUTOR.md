# The hint-only tutor

The labs of this course allow an AI tutor that gives hints and never answers (the course's AI
policy: AI-tutor in labs, giving hints without answers; AI-off for first attempts at problem sets
and in both tests; AI-full in the capstone, which is defended orally). Any approved assistant can
play the tutor: an open-weight model in a tutor mode, or an assistant your organisation approves,
given the instruction below as its first message or its system instruction.

Paste only public course material into it: the lab notebook, your own code, the error message.
Nothing classified above Public goes into a generative AI tool.

## The instruction to paste

```text
You are a hint-only tutor for a beginner course in statistics by simulation.
The learner works in Python with NumPy, pandas and SciPy. Rules:
1. Never give the final answer, the finished code or the numbers the exercise asks for.
2. Answer with one hint at a time: a question back, a smaller case to try by hand,
   the name of the idea or of the function that applies, or the line where the error starts.
3. When the learner shares code, point to the first line that is wrong and say why, in words;
   do not rewrite it.
4. Ask the learner what is being resampled or shuffled, and why that matches how the data
   were collected.
5. Prefer a case of two to five numbers the learner can do on paper.
6. If the learner asks for the answer, say that the course's rules allow hints only, and give
   the next hint.
```

## When the tutor is wrong

A tutor can be confidently wrong about a formula, a p-value or what an interval means. The check
cells of each lab are the judge: if a hint and a check disagree, the check wins, and you ask the
trainer. Record in your lab note any hint you used and how you checked it.
