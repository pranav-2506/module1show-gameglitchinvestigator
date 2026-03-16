# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

1. the counter stayed at the same number after the first attempt, should have decremented
2. the range was 1-100 but I was able to enter negative numbers, there should be a guardrail
3. the new game button was non functional after gameover, it should have reset the counter
4. the easy medium and difficult modes don't change the range displayed on the screen
5. the go lower and go higher hints were reversed
6. attempts went to negative after the fix

---

## 2. How did you use AI as a teammate?

- I used claude for this project
- one of the fixes, "Root cause: the outcome label ("Too High" / "Too Low") described the guess correctly, but the hint message told the player to move in the same wrong direction — 

"your guess is too high → go higher" is the opposite of what you want. Fixed both the try branch and the except TypeError fallback (which handles the string-comparison path on even attempts)." 

was correct the first go and it made the necessary changes

- when claude fixed the negative attempts, it suggested a change that let the attempts go to negative, so when i verified the bug which was 

"st.session_state.attempts += 1 fires unconditionally at the top of the submit block — even for invalid inputs (empty, non-number, out-of-range). Those invalid guesses never reach the game-over check (which lives in the else branch), so attempts keeps climbing past attempt_limit with no status change, making attempt_limit - attempts go negative."

and the fix was to move the increment inside the else block so only valid guesses cost an attempt. 
I later verified this by using the streamlit run command and actually testing out these changes myself.

---

## 3. Debugging and testing your fixes

- I tested the code manually by running the game and also ran valid pytests which helped me verify the code
- ran test_too_high_message_says_go_lower() in tests/test_game_logic.py using pytest. The test calls check_guess(75, 50) — a guess of 75 against a secret of 50 — and unpacks the returned tuple to check both the outcome label and the hint message:

outcome, message = check_guess(75, 50)
assert outcome == "Too High"
assert "LOWER" in message
assert "HIGHER" not in message
What it showed me: the existing tests only checked the first value of the tuple ("Too High") and passed fine even with the bug in place. Once I wrote a test that also checked the message string, I could see immediately that the original code returned "Go HIGHER!" when the player's guess was already too high , the exact opposite of what the player needed to hear.

- Did AI help you design or understand any tests? How?
Claude Code pointed out that check_guess returns a tuple (outcome, message) and that the preexisting tests compared the whole result to a plain string like "Too High" which would never even match a tuple, meaning those tests were actually broken in a different way too. Claude suggested writing tests that explicitly unpack both values and assert the message direction separately from the outcome label. That design choice, testing the message content independently, is what made the swapped hint bug detectable by a test at all.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
Every time I clicked a button or typed something, Streamlit ran the whole script from top to bottom again. The line random.randint(low, high) was just sitting there at the top with no protection around it, so every rerun rolled a new random number. The secret was never actually saved anywhere, it just kept getting replaced.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Imagine every time you clicked a button on a webpage, the entire page script restarted from scratch, like refreshing the page but keeping the same layout. That's basically what Streamlit does. Every interaction triggers a full rerun of your Python file. Session state is basically a small notebook that Streamlit keeps around between those reruns so your data survives. Without it everything resets to zero every single click.
- What change did you make that finally gave the game a stable secret number?
Wrapping the random.randint call inside an if "secret" not in st.session_state check. That way the first time the app loads it picks a number and saves it to session state, but every rerun after that skips over it because the key already exists. The secret stays locked in until you explicitly reset it, like when the new game button runs.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
have a structured approach like spotting the bugs and adding fix me and then working on fixes separately using separate sessions for each bug. This structure is something i plan on using for future projects. and obviously using git for version control is also something that i have been using and will continue to use 
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
I'd run the app manually after each individual fix instead of batching them together. A few times I wasn't sure if a bug was actually gone or just masked by something else. Testing one change at a time would make it way easier to know exactly what worked and what didn't.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
I used to assume AI code was either fully right or obviously broken but this project showed me it can be kinda wrong in ways that look completely fine at first glance.
