# # # File: src/crop_analytics.py
# # import streamlit as st
# # import pandas as pd
# # import plotly.graph_objects as go

# # def render_crop_analytics():
# #     # --- Custom CSS for Dark Theme & Styling ---
# #     st.markdown("""
# #     <style>
# #     /* Main Background */
# #     .stApp {
# #         background-color: #0e1117;
# #         color: white;
# #     }
# #     /* Cards/Metrics Styling */
# #     div[data-testid="stMetric"] {
# #         background-color: #1f2937;
# #         padding: 15px;
# #         border-radius: 10px;
# #         border: 1px solid #374151;
# #     }
# #     div[data-testid="stMetricLabel"] {
# #         color: #9ca3af;
# #     }
# #     div[data-testid="stMetricValue"] {
# #         color: white;
# #         font-size: 24px;
# #     }
# #     /* Input Fields */
# #     .stTextInput>div>div>input {
# #         color: white;
# #         background-color: #374151;
# #     }
# #     </style>
# #     """, unsafe_allow_html=True)

# #     st.title("Crop Analytics")
# #     st.caption("Data and insights based on your active crop inputs.")

# #     # --- 1. User Input Section ---
# #     # We use an expander so the inputs don't clutter the view once set
# #     with st.expander("📝 Update Crop Data (User Inputs)", expanded=True):
# #         col1, col2, col3 = st.columns(3)
# #         with col1:
# #             crop_name = st.text_input("Active Crop", value="Rice")
# #             # Stages: Seedling -> Vegetative -> Flowering -> Ripening
# #             current_stage = st.selectbox("Growth Stage", 
# #                 ["Seedling", "Vegetative", "Flowering", "Ripening"], 
# #                 index=2
# #             )
# #         with col2:
# #             days_in_stage = st.number_input("Days in Current Stage", value=12, step=1)
# #             growth_rate = st.slider("Avg Growth Rate (cm/day)", 0.0, 10.0, 1.2)
# #         with col3:
# #             water_level = st.slider("Current Water Level (cm)", 0, 20, 7)
# #             soil_moisture = st.slider("Soil Moisture (%)", 0, 100, 65)

# #     st.markdown("---")

# #     # --- 2. Growth Stage Visualization ---
# #     st.subheader(f"Growth Stage: {crop_name} ({current_stage})")
    
# #     # Calculate progress bar value based on stage
# #     stages_list = ["Seedling", "Vegetative", "Flowering", "Ripening"]
# #     try:
# #         progress_idx = stages_list.index(current_stage)
# #         progress_val = (progress_idx + 1) / len(stages_list)
# #     except:
# #         progress_val = 0.5
    
# #     st.progress(progress_val)
    
# #     # Dynamic description logic
# #     stage_info = {
# #         "Seedling": "Sensitive phase. Keep water shallow and protect from pests.",
# #         "Vegetative": "Active growing phase. High Nitrogen demand.",
# #         "Flowering": "Critical for yield. Avoid water stress and monitor for borers.",
# #         "Ripening": "Grain filling. Gradually reduce water before harvest."
# #     }
# #     st.info(stage_info.get(current_stage, "Monitor crop health regularly."))

# #     # --- 3. Key Metrics Grid ---
# #     m1, m2, m3, m4 = st.columns(4)
# #     m1.metric("Days in Stage", f"{days_in_stage} Days", delta="On Track")
# #     m2.metric("Expected Harvest", "4-5 Weeks", delta="Est.")
# #     m3.metric("Water Needs", "High", f"{water_level} cm (Current)")
# #     m4.metric("Nutrient Focus", "Phosphorus & Potassium")

# #     st.markdown("###") # Spacer

# #     # --- 4. Analytics Charts & Recommendations ---
# #     c1, c2 = st.columns([2, 1])

# #     with c1:
# #         st.subheader("Historical Growth & Water Trends")
        
# #         # Mock Data Generator based on inputs to make the chart look "alive"
# #         weeks = [1, 2, 3, 4, 5, 6]
# #         # Generate some mock history that ends at the current user input values
# #         growth_data = [x * (growth_rate * 0.8) for x in weeks] 
# #         water_data = [water_level + (x % 2 - 0.5) for x in weeks] # slightly fluctuating water

# #         fig = go.Figure()
        
# #         # Growth Line (Green)
# #         fig.add_trace(go.Scatter(
# #             x=weeks, y=growth_data, mode='lines+markers', name='Growth (cm)',
# #             line=dict(color='#2ecc71', width=3)
# #         ))
        
# #         # Water Level Line (Blue)
# #         fig.add_trace(go.Scatter(
# #             x=weeks, y=water_data, mode='lines+markers', name='Water Lvl (cm)',
# #             line=dict(color='#3498db', width=3)
# #         ))

# #         fig.update_layout(
# #             paper_bgcolor='rgba(0,0,0,0)',
# #             plot_bgcolor='rgba(255,255,255,0.05)',
# #             font=dict(color="white"),
# #             xaxis_title="Past Weeks",
# #             yaxis_title="Value",
# #             margin=dict(l=20, r=20, t=20, b=20),
# #             legend=dict(orientation="h", y=1.1)
# #         )
# #         st.plotly_chart(fig, use_container_width=True)

# #     with c2:
# #         st.subheader("AI Recommendations")
        
# #         # Dynamic advice based on user inputs
# #         recommendations = []
# #         if current_stage == "Flowering":
# #             recommendations.append("Apply Potassium to boost grain filling.")
# #             recommendations.append("Ensure water level stays above 5cm.")
# #         elif current_stage == "Vegetative":
# #              recommendations.append("Apply Urea (Nitrogen) for leaf growth.")
        
# #         if soil_moisture < 40:
# #              recommendations.append("⚠️ Soil moisture low! Irrigate immediately.")
# #         elif water_level > 10:
# #              recommendations.append("⚠️ Water level too high. Drain excess.")
             
# #         if not recommendations:
# #             recommendations.append("Maintain current care routine.")

# #         # Display recommendations
# #         for rec in recommendations:
# #             st.warning(f"• {rec}") if "⚠️" in rec else st.success(f"• {rec}")

# # File: src/crop_analytics.py
# import streamlit as st
# import pandas as pd
# import plotly.graph_objects as go

# # Update function to accept user_data
# def render_crop_analytics(user_data=None):
#     # Default values if no data is provided
#     default_crop = "Rice"
#     default_soil = "Clay"
    
#     # If we have database data, use it
#     if user_data:
#         default_crop = user_data.get('crop_type', 'Rice')
#         default_soil = user_data.get('soil_type', 'Clay')

#     st.markdown("""
#     <style>
#     .stApp { background-color: #0e1117; color: white; }
#     div[data-testid="stMetric"] { background-color: #1f2937; border: 1px solid #374151; }
#     </style>
#     """, unsafe_allow_html=True)

#     st.title("Crop Analytics")
    
#     # --- 1. User Inputs (Pre-filled from DB) ---
#     with st.expander("📝 Update Crop Data", expanded=False):
#         col1, col2 = st.columns(2)
#         with col1:
#             # use key='...' to ensure streamlit doesn't lose sync
#             crop_name = st.text_input("Active Crop", value=default_crop)
#             current_stage = st.selectbox("Growth Stage", ["Seedling", "Vegetative", "Flowering", "Ripening"], index=2)
#         with col2:
#             days_in_stage = st.number_input("Days in Stage", value=12)
#             water_level = st.slider("Water Level (cm)", 0, 15, 7)

#     # --- 2. Dashboard Logic (Same as before) ---
#     st.subheader(f"Analysis for: {crop_name}")
    
#     # Simple Progress Bar
#     stages = ["Seedling", "Vegetative", "Flowering", "Ripening"]
#     try:
#         progress = (stages.index(current_stage) + 1) / 4
#     except:
#         progress = 0.5
#     st.progress(progress)
#     st.caption(f"Current Stage: {current_stage} | Soil Context: {default_soil}")

#     # Metrics
#     m1, m2, m3 = st.columns(3)
#     m1.metric("Days in Stage", f"{days_in_stage} Days")
#     m2.metric("Water Level", f"{water_level} cm", delta="-2cm (Target 5cm)")
#     m3.metric("Soil Type", default_soil)

#     # Chart
#     st.subheader("Growth Trend")
#     chart_data = pd.DataFrame({
#         'Week': [1, 2, 3, 4, 5],
#         'Growth': [2, 4, 6, 8, 10] # Mock data
#     })
#     st.line_chart(chart_data.set_index('Week'))

