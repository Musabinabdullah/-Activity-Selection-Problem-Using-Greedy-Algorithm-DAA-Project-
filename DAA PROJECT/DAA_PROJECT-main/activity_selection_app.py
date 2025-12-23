# activity_selection_app.py - COMPLETE Streamlit Web Application
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np
from datetime import datetime

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Activity Selection Solver",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CORE ALGORITHM ====================
def greedy_activity_selection(activities):
    """Greedy algorithm for activity selection problem"""
    if not activities:
        return [], []
    
    # Sort by end time
    sorted_activities = sorted(activities, key=lambda x: x[2])
    selected = [sorted_activities[0]]
    last_idx = 0
    
    # Greedy selection
    for i in range(1, len(sorted_activities)):
        if sorted_activities[i][1] >= sorted_activities[last_idx][2]:
            selected.append(sorted_activities[i])
            last_idx = i
    
    return sorted_activities, selected

# ==================== STREAMLIT APP ====================
def main():
    # Title and description
    st.title("🎯 Activity Selection Problem - Greedy Algorithm")
    st.markdown("**Course: Design Analysis and Algorithms | Web Application**")
    st.markdown("---")
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        input_method = st.radio(
            "Select input method:",
            ["📚 Predefined Examples", "✏️ Manual Entry", "🎲 Random Generation"]
        )
        
        activities = []
        
        if input_method == "📚 Predefined Examples":
            example_choice = st.selectbox(
                "Choose example:",
                ["Standard Textbook (11 activities)",
                 "All Compatible (4 activities)", 
                 "All Overlapping (4 activities)"]
            )
            
            if example_choice == "Standard Textbook (11 activities)":
                activities = [
                    ("A1", 1, 4), ("A2", 3, 5), ("A3", 0, 6),
                    ("A4", 5, 7), ("A5", 3, 9), ("A6", 5, 9),
                    ("A7", 6, 10), ("A8", 8, 11), ("A9", 8, 12),
                    ("A10", 2, 14), ("A11", 12, 16)
                ]
            elif example_choice == "All Compatible (4 activities)":
                activities = [("B1", 1, 3), ("B2", 4, 6), ("B3", 7, 9), ("B4", 10, 12)]
            else:  # All Overlapping
                activities = [("C1", 2, 6), ("C2", 3, 7), ("C3", 4, 8), ("C4", 5, 9)]
                
        elif input_method == "✏️ Manual Entry":
            num_activities = st.number_input("Number of activities:", 1, 20, 5)
            
            for i in range(num_activities):
                cols = st.columns(3)
                with cols[0]:
                    act_id = st.text_input(f"ID {i+1}", value=f"A{i+1}", key=f"id_{i}")
                with cols[1]:
                    start = st.number_input(f"Start {i+1}", 0, 100, i*2, key=f"start_{i}")
                with cols[2]:
                    end = st.number_input(f"End {i+1}", start+1, 100, start+2, key=f"end_{i}")
                
                if act_id and start < end:
                    activities.append((act_id, start, end))
                    
        else:  # Random Generation
            num_random = st.slider("Number of activities:", 3, 20, 8)
            max_time = st.slider("Maximum time:", 10, 50, 24)
            
            if st.button("Generate Random"):
                activities = []
                for i in range(num_random):
                    start = np.random.randint(0, max_time-3)
                    end = start + np.random.randint(1, 5)
                    activities.append((f"R{i+1}", start, end))
    
    # Main content area
    if activities:
        # Run algorithm
        sorted_activities, selected = greedy_activity_selection(activities)
        
        # Display results in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 All Activities (Sorted by End Time)")
            df_all = pd.DataFrame(
                sorted_activities,
                columns=["Activity ID", "Start Time", "End Time"]
            )
            df_all["Duration"] = df_all["End Time"] - df_all["Start Time"]
            st.dataframe(df_all, use_container_width=True)
            
            # Algorithm stats
            st.metric("Total Activities", len(activities))
        
        with col2:
            st.subheader("✅ Selected Activities")
            if selected:
                df_selected = pd.DataFrame(
                    selected,
                    columns=["Activity ID", "Start Time", "End Time"]
                )
                df_selected["Duration"] = df_selected["End Time"] - df_selected["Start Time"]
                st.dataframe(df_selected, use_container_width=True)
                
                st.metric("Maximum Non-Overlapping Activities", len(selected))
                st.metric("Selection Ratio", f"{(len(selected)/len(activities))*100:.1f}%")
            else:
                st.warning("No compatible activities found!")
        
        # Visualization
        st.subheader("📊 Activity Timeline")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        colors = plt.cm.Set2(np.linspace(0, 1, len(activities)))
        
        # Plot each activity
        for i, (act_id, start, end) in enumerate(sorted(activities, key=lambda x: x[1])):
            # Color: green for selected, red for not selected
            color = 'green' if (act_id, start, end) in selected else 'red'
            alpha = 0.8 if (act_id, start, end) in selected else 0.3
            
            # Create rectangle for activity
            rect = patches.Rectangle(
                (start, i-0.3), end-start, 0.6,
                linewidth=2, edgecolor='black', facecolor=color, alpha=alpha
            )
            ax.add_patch(rect)
            
            # Add activity label
            ax.text(start + (end-start)/2, i, act_id,
                   ha='center', va='center', fontweight='bold', fontsize=10)
        
        ax.set_xlabel('Time', fontsize=12)
        ax.set_ylabel('Activities', fontsize=12)
        ax.set_title('Gantt Chart: Selected vs Non-Selected Activities', fontsize=14, pad=20)
        ax.set_yticks(range(len(activities)))
        ax.set_yticklabels([act[0] for act in sorted(activities, key=lambda x: x[1])])
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_xlim(0, max(end for _, _, end in activities) + 2)
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='green', alpha=0.8, edgecolor='black', label='Selected'),
            Patch(facecolor='red', alpha=0.3, edgecolor='black', label='Not Selected')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        st.pyplot(fig)
        
        # Algorithm explanation (expandable)
        with st.expander("📚 Algorithm Explanation & Complexity Analysis", expanded=False):
            st.markdown("""
            ### Greedy Algorithm Steps:
            1. **Sort** all activities by their finish time in non-decreasing order
            2. **Select** the first activity (earliest finish time)
            3. **Iterate** through remaining activities:
               - If activity's start time ≥ finish time of last selected activity
               - **Select** this activity
               - Update last selected activity
            
            ### Complexity Analysis:
            - **Time Complexity**: O(n log n) for sorting + O(n) for selection = **O(n log n)**
            - **Space Complexity**: O(n) for storing activities
            
            ### Why Greedy Works:
            The greedy choice (earliest finish time) always leaves the maximum possible 
            remaining time for future activities. This can be proven optimal using the 
            "greedy stays ahead" argument.
            """)
            
            # Step-by-step visualization
            st.subheader("🎯 Step-by-Step Selection Process")
            if selected:
                steps_html = "<div style='background-color:#f0f2f6; padding:15px; border-radius:10px;'>"
                last_end = -1
                for i, (act_id, start, end) in enumerate(selected):
                    steps_html += f"""
                    <div style='margin:10px 0; padding:10px; border-left:4px solid #4CAF50; background-color:white;'>
                        <b>Step {i+1}: Select Activity {act_id}</b><br>
                        • Time: [{start}, {end}]<br>
                        • Compatible with previous: {'Yes' if start >= last_end else 'N/A'}<br>
                        • Remaining time for next: {end} +
                    </div>
                    """
                    last_end = end
                steps_html += "</div>"
                st.markdown(steps_html, unsafe_allow_html=True)
    
    else:
        # Welcome message when no activities loaded
        st.info("👈 **Welcome!** Use the sidebar to configure your activities.")
        st.markdown("""
        ### How to use this application:
        1. **Choose an input method** from the sidebar
        2. **Configure your activities** (predefined, manual, or random)
        3. **View results** including:
           - All activities sorted by finish time
           - Selected non-overlapping activities
           - Interactive Gantt chart visualization
           - Algorithm explanation
        
        ### Features:
        - **Three input methods** for flexibility
        - **Real-time algorithm execution**
        - **Visual timeline** showing selected vs non-selected
        - **Complexity analysis** and step-by-step explanation
        """)
    
    # Footer
    st.markdown("---")
    st.caption(f"© {datetime.now().year} | Undergraduate Course Project - Design Analysis and Algorithms | Built with Streamlit")

# Run the app
if __name__ == "__main__":
    main()