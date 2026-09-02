import streamlit as st

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯",
    layout="wide"
)

# ---------- HEADER ----------

st.title("🎯 AI Interview Coach")
st.subheader("Interview Performance Scoreboard")

st.divider()

# ---------- MOCK DATA ----------
# Temporary data only.
# Integration will be added later.

before = {
    "Technical Knowledge": 4,
    "Communication": 3,
    "Problem Solving": 3,
    "Job Relevance": 1
}

after = {
    "Technical Knowledge": 8,
    "Communication": 9,
    "Problem Solving": 9,
    "Job Relevance": 8
}

# ---------- CALCULATE ----------

before_score = sum(before.values()) / len(before) * 10
after_score = sum(after.values()) / len(after) * 10
improvement = after_score - before_score

# ---------- OVERVIEW ----------

st.subheader("Performance Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "BEFORE SCORE",
        f"{before_score:.0f}/100"
    )

with col2:
    st.metric(
        "AFTER SCORE",
        f"{after_score:.0f}/100"
    )

with col3:
    st.metric(
        "IMPROVEMENT",
        f"+{improvement:.0f}"
    )

st.divider()

# ---------- CATEGORY SCORES ----------

st.subheader("Category-wise Performance")

for category in before:

    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        st.write(f"**{category}**")
        st.write(f"Before: {before[category]}/10")
        st.progress(before[category] / 10)

    with col2:
        st.write(" ")
        st.write(f"After: {after[category]}/10")
        st.progress(after[category] / 10)

    with col3:
        change = after[category] - before[category]
        st.metric("Change", f"+{change}")

    st.divider()

# ---------- OVERALL COMPARISON ----------

st.subheader("Overall Performance")

col1, col2 = st.columns(2)

with col1:
    st.write("### Before")
    st.progress(before_score / 100)
    st.write(f"**{before_score:.0f}%**")

with col2:
    st.write("### After")
    st.progress(after_score / 100)
    st.write(f"**{after_score:.0f}%**")

st.divider()

# ---------- FINAL RESULT ----------

st.subheader("🎯 Final Result")

st.success(
    f"Overall improvement: +{improvement:.0f} percentage points"
)
