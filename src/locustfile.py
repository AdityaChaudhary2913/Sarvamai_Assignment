from locust import HttpUser, task, between
import os

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

if not SARVAM_API_KEY:
    print("[WARNING]: SARVAM_API_KEY is not set in the environment variables!")

class STUser(HttpUser):
    # For 4th configuration, i have to use wait time between(5, 10), because i was getting error that "too many request"
    # For configuration 1, 2, 3 i have used wait time between(2, 5)
    wait_time = between(4, 8)
    host = "https://api.sarvam.ai"
    
    def on_start(self):
        if not SARVAM_API_KEY:
            self.environment.process_exit_code = 1
            raise Exception("SARVAM_API_KEY is not set. Cannot proceed with tests!")
    
    @task
    def transliterate_bengali_to_english(self):
        headers = {
            "api-subscription-key": SARVAM_API_KEY,
            "Content-Type": "application/json",
        }
        payload = {
            "input": "নমস্কার", # Bengali for "Namaskar"
            "source_language_code": "bn-IN",
            "target_language_code": "en-IN"
        }
        self.client.post('/transliterate', json=payload, headers=headers, name="Bengali")

    @task
    def transliterate_gujarati_to_english(self):
        headers = {
            "api-subscription-key": SARVAM_API_KEY,
            "Content-Type": "application/json",
        }
        payload = {
            "input": "કેમ છો", # Gujarati for "Kem Cho" (How are you?)
            "source_language_code": "gu-IN",
            "target_language_code": "en-IN"
        }
        self.client.post('/transliterate', json=payload, headers=headers, name="Gujarati")

    @task
    def transliterate_hindi_to_english(self):
        headers = {
            "api-subscription-key": SARVAM_API_KEY,
            "Content-Type": "application/json",
        }
        payload = {
            "input": "नमस्ते", # Hindi for "Namaste"
            "source_language_code": "hi-IN",
            "target_language_code": "en-IN"
        }
        self.client.post('/transliterate', json=payload, headers=headers, name="Hindi")

    @task
    def transliterate_kannada_to_english(self):
        headers = {
            "api-subscription-key": SARVAM_API_KEY,
            "Content-Type": "application/json",
        }
        payload = {
            "input": "ನಮಸ್ಕಾರ", # Kannada for "Namaskara"
            "source_language_code": "kn-IN",
            "target_language_code": "en-IN"
        }
        self.client.post('/transliterate', json=payload, headers=headers, name="Kannada")

    @task
    def transliterate_malayalam_to_english(self):
        headers = {
            "api-subscription-key": SARVAM_API_KEY,
            "Content-Type": "application/json",
        }
        payload = {
            "input": "നമസ്കാരം", # Malayalam for "Namaskaram"
            "source_language_code": "ml-IN",
            "target_language_code": "en-IN"
        }
        self.client.post('/transliterate', json=payload, headers=headers, name="Malayalam")

    @task
    def transliterate_marathi_to_english(self):
        headers = {
            "api-subscription-key": SARVAM_API_KEY,
            "Content-Type": "application/json",
        }
        payload = {
            "input": "नमस्कार", # Marathi for "Namaskar"
            "source_language_code": "mr-IN",
            "target_language_code": "en-IN"
        }
        self.client.post('/transliterate', json=payload, headers=headers, name="Marathi")

    @task
    def transliterate_odia_to_english(self):
        headers = {
            "api-subscription-key": SARVAM_API_KEY,
            "Content-Type": "application/json",
        }
        payload = {
            "input": "ନମସ୍କାର", # Odia for "Namaskara"
            "source_language_code": "od-IN",
            "target_language_code": "en-IN"
        }
        self.client.post('/transliterate', json=payload, headers=headers, name="Odia")

    @task
    def transliterate_punjabi_to_english(self):
        headers = {
            "api-subscription-key": SARVAM_API_KEY,
            "Content-Type": "application/json",
        }
        payload = {
            "input": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ", # Punjabi for "Sat Sri Akal"
            "source_language_code": "pa-IN",
            "target_language_code": "en-IN"
        }
        self.client.post('/transliterate', json=payload, headers=headers, name="Punjabi")

    @task
    def transliterate_tamil_to_english(self):
        headers = {
            "api-subscription-key": SARVAM_API_KEY,
            "Content-Type": "application/json",
        }
        payload = {
            "input": "வணக்கம்", # Tamil for "Vanakkam"
            "source_language_code": "ta-IN",
            "target_language_code": "en-IN"
        }
        self.client.post('/transliterate', json=payload, headers=headers, name="Tamil")

    @task
    def transliterate_telugu_to_english(self):
        headers = {
            "api-subscription-key": SARVAM_API_KEY,
            "Content-Type": "application/json",
        }
        payload = {
            "input": "నమస్కారం", # Telugu for "Namaskaram"
            "source_language_code": "te-IN",
            "target_language_code": "en-IN"
        }
        self.client.post('/transliterate', json=payload, headers=headers, name="Telugu")