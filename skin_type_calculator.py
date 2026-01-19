import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Skin Type Calculator",
    page_icon="👩‍⚕️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF6B8B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .skin-type-card {
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .question-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Skin type definitions
SKIN_TYPES = {
    "Normal": {
        "description": "Well-balanced skin - not too oily, not too dry",
        "characteristics": ["Few imperfections", "No severe sensitivity", "Barely visible pores", "Radiant complexion"],
        "color": "#4CAF50"
    },
    "Oily": {
        "description": "Excess sebum production, shiny appearance",
        "characteristics": ["Enlarged pores", "Prone to blackheads and acne", "Makeup doesn't stay put", "Thick complexion"],
        "color": "#2196F3"
    },
    "Dry": {
        "description": "Lacks moisture and lipids to retain moisture",
        "characteristics": ["Almost invisible pores", "Red patches", "Less elastic skin", "More visible lines"],
        "color": "#FF9800"
    },
    "Combination": {
        "description": "Oily in T-zone, dry/normal on cheeks",
        "characteristics": ["Oily T-zone", "Dry cheeks", "Enlarged pores in T-zone", "Prone to blackheads"],
        "color": "#9C27B0"
    },
    "Sensitive": {
        "description": "Reacts easily to products and environmental factors",
        "characteristics": ["Redness", "Itching", "Burning sensation", "Dryness"],
        "color": "#F44336"
    }
}

class SkinTypeCalculator:
    def __init__(self):
        self.questions = self.load_questions()
        self.results_df = pd.DataFrame(columns=['Skin Type', 'Score'])
        
    def load_questions(self):
        return [
            {
                "id": 1,
                "question": "How does your skin feel a few hours after cleansing?",
                "options": {
                    "Tight and dry": {"Dry": 2, "Normal": 0, "Oily": 0, "Combination": 1, "Sensitive": 1},
                    "Comfortable, not oily": {"Dry": 0, "Normal": 2, "Oily": 0, "Combination": 1, "Sensitive": 1},
                    "Shiny all over": {"Dry": 0, "Normal": 0, "Oily": 2, "Combination": 1, "Sensitive": 0},
                    "Shiny in T-zone only": {"Dry": 0, "Normal": 1, "Oily": 1, "Combination": 2, "Sensitive": 0}
                }
            },
            {
                "id": 2,
                "question": "How visible are your pores?",
                "options": {
                    "Almost invisible": {"Dry": 2, "Normal": 0, "Oily": 0, "Combination": 0, "Sensitive": 1},
                    "Visible but small": {"Dry": 0, "Normal": 2, "Oily": 0, "Combination": 1, "Sensitive": 1},
                    "Clearly visible, enlarged": {"Dry": 0, "Normal": 0, "Oily": 2, "Combination": 1, "Sensitive": 0},
                    "Large in T-zone only": {"Dry": 0, "Normal": 0, "Oily": 1, "Combination": 2, "Sensitive": 0}
                }
            },
            {
                "id": 3,
                "question": "How does your skin react to new products?",
                "options": {
                    "Usually no reaction": {"Dry": 1, "Normal": 2, "Oily": 1, "Combination": 1, "Sensitive": 0},
                    "Gets slightly red": {"Dry": 1, "Normal": 0, "Oily": 0, "Combination": 1, "Sensitive": 2},
                    "Breaks out": {"Dry": 0, "Normal": 0, "Oily": 2, "Combination": 1, "Sensitive": 1},
                    "Gets dry/flaky": {"Dry": 2, "Normal": 0, "Oily": 0, "Combination": 1, "Sensitive": 1}
                }
            },
            {
                "id": 4,
                "question": "How does your skin feel in the afternoon?",
                "options": {
                    "Tight and uncomfortable": {"Dry": 2, "Normal": 0, "Oily": 0, "Combination": 1, "Sensitive": 1},
                    "Comfortable": {"Dry": 0, "Normal": 2, "Oily": 0, "Combination": 1, "Sensitive": 1},
                    "Shiny and oily": {"Dry": 0, "Normal": 0, "Oily": 2, "Combination": 1, "Sensitive": 0},
                    "Oily only in T-zone": {"Dry": 0, "Normal": 1, "Oily": 1, "Combination": 2, "Sensitive": 0}
                }
            },
            {
                "id": 5,
                "question": "How often do you experience breakouts?",
                "options": {
                    "Rarely or never": {"Dry": 1, "Normal": 2, "Oily": 0, "Combination": 1, "Sensitive": 1},
                    "Occasionally": {"Dry": 1, "Normal": 1, "Oily": 1, "Combination": 2, "Sensitive": 1},
                    "Frequently": {"Dry": 0, "Normal": 0, "Oily": 2, "Combination": 1, "Sensitive": 0},
                    "Only in T-zone": {"Dry": 0, "Normal": 0, "Oily": 1, "Combination": 2, "Sensitive": 0}
                }
            }
        ]
    
    def calculate_skin_type(self, answers):
        scores = {skin_type: 0 for skin_type in SKIN_TYPES.keys()}
        
        for question_id, answer in answers.items():
            question = next(q for q in self.questions if q["id"] == question_id)
            if answer in question["options"]:
                for skin_type, score in question["options"][answer].items():
                    scores[skin_type] += score
        
        return scores
    
    def determine_primary_type(self, scores):
        return max(scores.items(), key=lambda x: x[1])
    
    def create_results_dataframe(self, scores):
        df = pd.DataFrame(list(scores.items()), columns=['Skin Type', 'Score'])
        df = df.sort_values('Score', ascending=False)
        return df
    
    def plot_results(self, scores):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Bar chart
        skin_types = list(scores.keys())
        values = list(scores.values())
        colors = [SKIN_TYPES[st]["color"] for st in skin_types]
        
        bars = ax1.bar(skin_types, values, color=colors, edgecolor='black')
        ax1.set_title('Skin Type Analysis Results', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Skin Types', fontsize=12)
        ax1.set_ylabel('Score', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{value}', ha='center', va='bottom', fontweight='bold')
        
        # Pie chart
        primary_type, primary_score = self.determine_primary_type(scores)
        sizes = [primary_score] + [sum(values) - primary_score]
        labels = [f'{primary_type}\n({primary_score} pts)', 'Other Types']
        colors_pie = [SKIN_TYPES[primary_type]["color"], '#CCCCCC']
        
        ax2.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%',
                startangle=90, explode=(0.1, 0), shadow=True)
        ax2.set_title(f'Primary Skin Type: {primary_type}', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        return fig

def main():
    st.markdown('<h1 class="main-header">🧬 Skin Type Calculator</h1>', unsafe_allow_html=True)
    
    # Initialize calculator
    calculator = SkinTypeCalculator()
    
    # Create two columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 Skin Assessment Questionnaire")
        st.write("Answer the following questions to determine your skin type:")
        
        answers = {}
        
        # Display questions
        for question in calculator.questions:
            with st.container():
                st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
                st.write(f"**Q{question['id']}: {question['question']}**")
                answer = st.radio(
                    f"Select your answer for Q{question['id']}:",
                    options=list(question["options"].keys()),
                    key=f"q{question['id']}",
                    label_visibility="collapsed"
                )
                answers[question["id"]] = answer
                st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### ℹ️ Skin Types Guide")
        for skin_type, info in SKIN_TYPES.items():
            with st.container():
                st.markdown(f'''
                <div class="skin-type-card" style="border-left: 5px solid {info['color']};">
                    <h4 style="color: {info['color']}; margin-top: 0;">{skin_type}</h4>
                    <p><strong>{info['description']}</strong></p>
                    <ul style="margin-bottom: 0;">
                ''', unsafe_allow_html=True)
                
                for char in info['characteristics']:
                    st.markdown(f'<li>{char}</li>', unsafe_allow_html=True)
                
                st.markdown('</ul></div>', unsafe_allow_html=True)
    
    # Calculate button
    if st.button("🧪 Calculate My Skin Type", type="primary", use_container_width=True):
        if len(answers) == len(calculator.questions):
            with st.spinner("Analyzing your skin type..."):
                # Calculate scores
                scores = calculator.calculate_skin_type(answers)
                primary_type, primary_score = calculator.determine_primary_type(scores)
                
                # Create results dataframe
                results_df = calculator.create_results_dataframe(scores)
                
                # Display results
                st.markdown("---")
                st.markdown(f"## 🎯 Your Results")
                
                result_col1, result_col2 = st.columns(2)
                
                with result_col1:
                    st.metric(
                        label="Primary Skin Type",
                        value=primary_type,
                        delta=f"{primary_score} points"
                    )
                    st.markdown(f"**Description:** {SKIN_TYPES[primary_type]['description']}")
                    
                    st.markdown("### 📊 Detailed Scores")
                    st.dataframe(
                        results_df,
                        column_config={
                            "Skin Type": "Skin Type",
                            "Score": st.column_config.NumberColumn(
                                "Score",
                                help="Higher score indicates stronger tendency"
                            )
                        },
                        hide_index=True,
                        use_container_width=True
                    )
                
                with result_col2:
                    # Display characteristics
                    st.markdown("### ✨ Characteristics")
                    for char in SKIN_TYPES[primary_type]['characteristics']:
                        st.write(f"✓ {char}")
                
                # Plot visualization
                st.markdown("### 📈 Visualization")
                fig = calculator.plot_results(scores)
                st.pyplot(fig)
                
                # Download options
                col1, col2 = st.columns(2)
                
                with col1:
                    # Download as CSV
                    csv = results_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results (CSV)",
                        data=csv,
                        file_name="skin_type_analysis.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                with col2:
                    # Download plot as PNG
                    buf = BytesIO()
                    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
                    buf.seek(0)
                    st.download_button(
                        label="🖼️ Download Plot (PNG)",
                        data=buf,
                        file_name="skin_type_analysis.png",
                        mime="image/png",
                        use_container_width=True
                    )
                
                # Recommendations
                st.markdown("### 💡 Recommendations for Your Skin Type")
                recommendations = {
                    "Normal": [
                        "Use gentle cleansers",
                        "Apply moisturizer daily",
                        "Use sunscreen regularly",
                        "Get regular facials for maintenance"
                    ],
                    "Oily": [
                        "Use oil-free, non-comedogenic products",
                        "Clean twice daily with gentle cleanser",
                        "Use clay masks weekly",
                        "Avoid heavy, oil-based products"
                    ],
                    "Dry": [
                        "Use cream-based cleansers",
                        "Apply rich moisturizers",
                        "Avoid hot showers",
                        "Use hydrating masks regularly"
                    ],
                    "Combination": [
                        "Treat different areas separately",
                        "Use gel-based moisturizers for T-zone",
                        "Use cream-based products for dry areas",
                        "Consider double cleansing method"
                    ],
                    "Sensitive": [
                        "Patch test all new products",
                        "Use fragrance-free products",
                        "Avoid harsh exfoliants",
                        "Stick to minimal product routine"
                    ]
                }
                
                for rec in recommendations[primary_type]:
                    st.write(f"• {rec}")
        else:
            st.error("⚠️ Please answer all questions before calculating!")
    
    # Information section
    with st.expander("ℹ️ About This Calculator"):
        st.markdown("""
        ### How the Calculator Works
        
        This skin type calculator uses a weighted scoring system based on dermatological principles:
        
        1. **Multiple Parameters**: Considers oil production, pore size, sensitivity, and more
        2. **Weighted Scoring**: Each answer contributes differently to various skin types
        3. **Comprehensive Analysis**: Results show your primary skin type with detailed breakdown
        
        ### Accuracy Note
        
        This tool provides general guidance. For professional diagnosis, consult a dermatologist.
        
        ### Skin Types Explained
        
        - **Normal**: Balanced skin with few issues
        - **Oily**: Excess sebum, prone to acne
        - **Dry**: Lacks moisture, may feel tight
        - **Combination**: Mix of oily and dry areas
        - **Sensitive**: Reacts easily to products
        """)

if __name__ == "__main__":
    main()