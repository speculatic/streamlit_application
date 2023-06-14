import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import io

web_apps = st.sidebar.selectbox("Select Web Apps",
                                ("Exploratory Data Analysis", "Distributions"))


if web_apps == "Exploratory Data Analysis":

  uploaded_file = st.sidebar.file_uploader("Choose a file")

  if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    df = pd.read_csv(uploaded_file)
    show_df = st.checkbox("Show Data Frame", key="disabled")

    if show_df:
      st.write(df)

    # Display relevant statistics about the dataset
    st.write('Number of Rows:', df.shape[0])
    st.write('Number of Columns:', df.shape[1])
    st.write('Number of Numerical Variables:', len(df.select_dtypes(include=['int64', 'float64']).columns))
    st.write('Number of Categorical Variables:', len(df.select_dtypes(include=['object']).columns))
    st.write('Number of Boolean Variables:', len(df.select_dtypes(include=['bool']).columns))

    column_type = st.sidebar.selectbox('Select Data Type',
                                       ("Numerical", "Categorical", "Bool", "Date"))

    if column_type == "Numerical":
      numerical_column = st.sidebar.selectbox(
          'Select a Column', df.select_dtypes(include=['int64', 'float64']).columns)

      # 5num Summary
      st.write(df[numerical_column].describe())

      # Distribution plot
      choose_color = st.color_picker('Pick a Color', "#69b3a2")
      choose_opacity = st.slider(
          'Color Opacity', min_value=0.0, max_value=1.0, step=0.05)
      hist_bins = st.slider('Number of bins', min_value=5,
                            max_value=150, value=30)
      hist_title = st.text_input('Set Title', 'Distribution Plot')
      hist_xtitle = st.text_input('Set x-axis Title', numerical_column)

      fig, ax = plt.subplots()
      sns.histplot(df[numerical_column], bins=hist_bins, kde=True, color=choose_color, ax=ax)
      ax.set_title(hist_title)
      ax.set_xlabel(hist_xtitle)
      ax.set_ylabel('Frequency')
      st.pyplot(fig)

    elif column_type == "Categorical":
      categorical_column = st.sidebar.selectbox(
          'Select a Column', df.select_dtypes(include=['object']).columns)

      # Proportion
      st.write(df[categorical_column].value_counts(normalize=True))

      # Barplot
      choose_color = st.color_picker('Pick a Color', "#69b3a2")
      fig, ax = plt.subplots()
      sns.countplot(x=categorical_column, data=df, color=choose_color, ax=ax)
      plt.xticks(rotation=90)
      st.pyplot(fig)
