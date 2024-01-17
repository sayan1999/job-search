# Job Apply

**GPT based generation of cover letters and LinkedIn referrals based on job descriptions and resumes.**

## Features

- **Cover Letter Generation:** Automatically creates tailored cover letters based on the provided job description and resume.
- **Referral Note Generation:** Crafts concise and polite LinkedIn referral notes to request connections for referrals.
- **Resume Improvement Suggestions:** Identifies potential skill gaps and suggests keywords to enhance your resume's alignment with job requirements.

## Usage

1. **Install Dependencies:**

   ```bash
   pip install streamlit google-generativeai
   ```

2. **Set Up Environment Variables:**
   Create a .env file in the project directory and add the following variables:
   ```
   RESUME=your_resume_url
   GOOGLE_API_KEY=your_google_api_key
   ```
3. **Run the App:**
   ```bash
   streamlit run app.py
   ```
4. **Navigation**
   Use the sidebar to select between "Cover Letter" and "LinkedIn Referral" functionalities.
