from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import threading
import time

app = Flask(__name__)

# Global cache
cached_jobs = []
CACHE_INTERVAL = 30  # seconds

def fetch_job_data():
    global cached_jobs
    print("🔄 Fetching job data...")

    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get("https://aristasystems.in/careers.php")
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        job_list = []

        job_items = soup.select("li.career_tab_list")
        for job in job_items:
            title_tag = job.select_one("span")
            job_title = title_tag.get_text(strip=True) if title_tag else "Unknown"
            rel_value = job.get("rel")

            job_detail_div = None
            for div in soup.select("div.tab_content"):
                class_list = div.get("class", [])
                if rel_value in class_list:
                    job_detail_div = div
                    break

            if not job_detail_div:
                continue

            experience = location = vacancies = qualification = ""
            responsibilities = []
            skills = []

            for span in job_detail_div.select("div.open_condi_col span"):
                text = span.get_text(strip=True)
                if "Experience:" in text:
                    experience = text.replace("Experience:", "").strip()
                elif "Job Location:" in text:
                    location = text.replace("Job Location:", "").strip()
                elif "No of Vacancies:" in text:
                    vacancies = text.replace("No of Vacancies:", "").strip()
                elif "Qualification:" in text:
                    qualification = text.replace("Qualification:", "").strip()

            for section in job_detail_div.select("div.open_condi_text"):
                heading = section.find("strong")
                if heading and "Roles & Responsibilities" in heading.text:
                    responsibilities = [li.get_text(strip=True) for li in section.find_all("li")]
                if heading and "Skills Required" in heading.text:
                    skills = [li.get_text(strip=True) for li in section.find_all("li")]

            job_list.append({
                "title": job_title,
                "experience_level": experience,
                "location": location,
                "vacancies": vacancies,
                "qualification": qualification,
                "responsibilities": responsibilities,
                "skills_required": skills
            })

        cached_jobs = job_list
        print(f"✅ Job cache updated with {len(cached_jobs)} entries.")

    except Exception as e:
        print(f"❌ Error while fetching job data: {e}")

# Background updater
def start_cache_updater():
    def update_loop():
        while True:
            fetch_job_data()
            time.sleep(CACHE_INTERVAL)

    updater_thread = threading.Thread(target=update_loop, daemon=True)
    updater_thread.start()

@app.route("/jobs/arista-jobs/available-roles", methods=["GET"])
def get_jobs():
    return jsonify({"jobs": cached_jobs})

def run_app():
    print("🚀 Starting app & pre-fetching data")
    fetch_job_data()
    start_cache_updater()
    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    run_app()
