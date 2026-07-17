# 💻 Laptop Recommendation System

## 📌 Project Overview

The **Laptop Recommendation System** is developed as part of the **DecodeLabs Artificial Intelligence Internship – Project 3**.

This project recommends laptops to users based on their preferences such as **company, laptop type, RAM, operating system, budget, and product search**. It uses a **filter-based recommendation approach**, allowing users to quickly find laptops that best match their requirements.

The application is built using **Python**, **Pandas**, and **Streamlit**, providing an interactive and user-friendly interface.

---

# 🎯 Project Objectives

* Build a recommendation system using a real-world dataset.
* Filter laptops based on user preferences.
* Display personalized laptop recommendations.
* Develop an interactive web application using Streamlit.
* Understand the fundamentals of recommendation systems.

---

# 📂 Dataset

**Dataset Name:** Laptop Price Dataset

The dataset contains detailed information about different laptop models from multiple manufacturers.

### Dataset Features

* Laptop ID
* Company
* Product Name
* Laptop Type
* Screen Size
* Screen Resolution
* Processor
* RAM
* Storage
* Graphics Card
* Operating System
* Weight
* Price (Euros)

---

# 🛠️ Technologies Used

* Python
* Streamlit
* Pandas

---

# 🚀 Features

* 📊 Dataset Preview
* 📈 Dataset Statistics
* 🔍 Product Search
* 🏢 Company Filter
* 💻 Laptop Type Filter
* 🧠 RAM Filter
* 🖥️ Operating System Filter
* 💰 Budget Filter
* 📋 Professional Recommendation Cards
* 📥 Download Recommendations as CSV
* 🎨 Responsive Streamlit User Interface

---

# ⚙️ Recommendation Workflow

```text
Load Dataset
      ↓
Data Cleaning
      ↓
User Selects Preferences
      ↓
Filter Dataset
      ↓
Find Matching Laptops
      ↓
Display Recommendations
```

---

# 🧠 Recommendation Logic

The recommendation system filters laptops based on:

* Company
* Laptop Type
* RAM
* Operating System
* Maximum Budget
* Product Search

Only laptops matching all selected preferences are displayed to the user.

---

# 📁 Project Structure

```text
Laptop-Recommendation-System/
│
├── app.py
├── laptop_price.csv
├── README.md
```

---

# ▶️ Installation

## Step 1

Clone the repository

```bash
git clone https://github.com/your-username/laptop-recommendation-system.git
```

## Step 2

Move into the project directory

```bash
cd laptop-recommendation-system
```

## Step 3

Install the required libraries

```bash
pip install -r requirements.txt
```

## Step 4

Run the Streamlit application

```bash
streamlit run app.py
```

---

# 💡 How to Use

1. Launch the application.
2. Choose your preferred laptop company.
3. Select the laptop type.
4. Choose the required RAM.
5. Select the operating system.
6. Adjust the maximum budget.
7. Optionally search by product name.
8. View the recommended laptops.
9. Download the filtered recommendations as a CSV file if needed.

---

# 📊 Application Features

The application provides:

* Total number of laptops
* Number of companies
* Average laptop price
* Minimum laptop price
* Maximum laptop price
* Interactive filtering
* Dynamic recommendations
* Download option

---

# 📸 Screenshots

Add screenshots of your application in the **screenshots/** folder.

---

# 🎓 Learning Outcomes

Through this project, I learned:

* Recommendation Systems
* Data Filtering
* Data Analysis using Pandas
* Streamlit Web Application Development
* Interactive Dashboard Design
* User Preference Matching
* Dataset Exploration
* CSV File Handling
* Python Programming

---

# 🔮 Future Improvements

* Content-Based Recommendation using Cosine Similarity
* Machine Learning Recommendation Engine
* Personalized User Profiles
* Favorite Laptop Feature
* Price Comparison
* Laptop Images
* Product Ratings
* Dark Mode
* Cloud Deployment using Streamlit Community Cloud
* Database Integration



# 📜 License

This project is developed for educational purposes as part of the **DecodeLabs Artificial Intelligence Internship – Project 3**.

---

# 🙏 Acknowledgements

* DecodeLabs
* Streamlit
* Pandas
* Kaggle (Laptop Price Dataset)
* Python Community
