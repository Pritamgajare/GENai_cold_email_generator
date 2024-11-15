import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://examplejobsite.com/jobs/software-engineer")
    submit_button = st.button("Submit")

    if submit_button:
        with st.spinner("Loading... Please wait."):
            try:
                # Set USER_AGENT environment variable if not already set
                import os
                if not os.getenv("USER_AGENT"):
                    os.environ["USER_AGENT"] = "ColdEmailGeneratorApp/1.0"

                # Load and process data
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)

                for job in jobs:
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links)
                    st.code(email, language='markdown')
            except Exception as e:
                st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)


# sample site
# https://jobs.nike.com/job/R-43503?from=job%20search%20funnel