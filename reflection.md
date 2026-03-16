# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

1. The hints were wrong. when the score was lower than the number, the hint would prompt the player to go higher and vice versa.
2. the range of numbers for easy, normal and hard were inconsistent. 1-20 for easy, 1-100 for normal and 1-50 for hard
3. The no. of attempts are inconsistent with the easy, normal and hard dynamic.
4. the no. of attempts are inconsistent with the no. of tries permitted.
5. new game button doesnt work.
6. changing difficulty doesnt start a new game with the selected difficulty.

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

1. I used copilot on this on this project
2. The AI suggested a fix for the hints

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

1. I tested it repeatedly against different inputs
2. after i ammended the code for the changing difficulty, i tested the change by running the game. during the game, i changed the difficulty mid game and it started a new game.

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
