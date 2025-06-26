import streamlit as st
from streamlit_timeline import st_timeline
import openai
import os
from datetime import date

# Set your OpenAI API key (use environment variable for security)
openai.api_key = os.getenv('OPENAI_API_KEY', '')

st.set_page_config(page_title="Project Timeline with AI Chat", layout="wide")
st.title("🚀 Project Timeline Portfolio")
st.write("Map out your career or project milestones. Click a node for details. Ask the AI chatbot about your journey!")

# Initialize timeline items in session state
if "timeline_items" not in st.session_state:
    st.session_state["timeline_items"] = []
    st.session_state["next_id"] = 1

# --- Timeline Item Form ---
st.sidebar.header("Add/Edit Timeline Item")
with st.sidebar.form("timeline_form", clear_on_submit=True):
    content = st.text_input("Title/Label", placeholder="e.g. Started University")
    start = st.date_input("Start Date", value=date.today())
    end_enabled = st.checkbox("Specify End Date?")
    end = st.date_input("End Date", value=date.today()) if end_enabled else None
    details = st.text_area("Details", placeholder="e.g. Description of this milestone or project")
    submitted = st.form_submit_button("Add Milestone")
    
    if submitted and content:
        item = {
            "id": st.session_state["next_id"],
            "content": content,
            "start": str(start),
            "title": details
        }
        if end_enabled and end:
            item["end"] = str(end)
        st.session_state["timeline_items"].append(item)
        st.session_state["next_id"] += 1
        st.success(f"Added: {content}")

# --- Timeline Display & Deletion ---
st.subheader("Your Timeline")
if st.session_state["timeline_items"]:
    selected = st_timeline(st.session_state["timeline_items"], groups=[], options={"selectable": True, "height": "350px"}, height="350px")
    if selected:
        selected_item = next((item for item in st.session_state["timeline_items"] if item["id"] == selected[0]), None)
        if selected_item:
            st.info(f"**{selected_item['content']}**: {selected_item.get('title', '')}")
            # Option to delete selected item
            if st.button(f"Delete '{selected_item['content']}'"):
                st.session_state["timeline_items"] = [item for item in st.session_state["timeline_items"] if item["id"] != selected_item["id"]]
                st.success(f"Deleted: {selected_item['content']}")
else:
    st.info("No milestones yet. Add your first one in the sidebar!")

st.markdown("---")
st.header("💬 Ask the AI about this timeline!")

# Simple chat interface
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

user_input = st.text_input("Ask a question about the timeline, resume, or projects:")
if st.button("Ask AI") and user_input:
    # Compose context for the AI
    context = "Here is a project/career timeline: "
    for item in st.session_state["timeline_items"]:
        context += f"\n- {item['content']} ({item['start']}{' to ' + item['end'] if 'end' in item else ''}): {item.get('title', '')}"
    context += f"\nUser question: {user_input}"
    
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert assistant that answers questions about the user's career/project timeline."},
                {"role": "user", "content": context}
            ],
            max_tokens=200
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        answer = f"Error: {e}"
    st.session_state["chat_history"].append((user_input, answer))

# Display chat history
for q, a in st.session_state["chat_history"]:
    st.markdown(f"**You:** {q}")
    st.markdown(f"**AI:** {a}") 