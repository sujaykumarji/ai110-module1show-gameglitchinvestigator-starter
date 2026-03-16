import random
import streamlit as st

# FIX: Moved all game logic to logic_utils.py using Claude Code to keep UI and
# logic separated. Import replaces the four functions that were previously defined here.
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
    key="difficulty",
)

attempt_limit_map = {
    "Easy": 8,
    "Normal": 6,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# If the user changed the difficulty since the last run, reset the game
if "prev_difficulty" not in st.session_state:
    st.session_state.prev_difficulty = difficulty
elif st.session_state.prev_difficulty != difficulty:
    st.session_state.prev_difficulty = difficulty
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.last_hint = None  # FIX: Clear stale hint when difficulty changes.
    st.success(f"Difficulty changed to {difficulty}. New game started.")
    st.rerun()

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

# FIX: Added last_hint to session_state so the hint message survives st.rerun().
# Without this, st.warning() called inside the submit block is wiped before rendering.
if "last_hint" not in st.session_state:
    st.session_state.last_hint = None

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

# FIX: Display hint stored from previous submit before rerun clears it.
# st.rerun() wipes any st.warning() called in the same run, so we persist
# the hint in session_state and render it here on the next pass.
if st.session_state.last_hint:
    st.warning(st.session_state.last_hint)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)


if new_game:
    # Reset game state and start a new secret within the current difficulty range
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.last_hint = None  # FIX: Clear stale hint on new game.
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        # Always use the numeric secret so comparisons remain numeric
        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        # FIX: Store hint in session_state instead of calling st.warning() directly.
        # st.rerun() at the end of this block would wipe any widget rendered here,
        # so we save to session_state and render it on the next pass above the input.
        if show_hint:
            st.session_state.last_hint = message
        else:
            st.session_state.last_hint = None

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

    # FIX: Added st.rerun() after every submit so the attempts counter and debug info
    # update immediately. Claude Code diagnosed that Streamlit renders top-to-bottom,
    # so st.info and the expander rendered with stale state before the submit handler ran.
    st.rerun()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
