import requests

# Ganti dengan API Key Groq Anda
API_KEY = "YOUR_GROQ_API_KEY" 
URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Payload seminimal mungkin agar tidak menguras token
payload = {
    "model": "llama-3.3-70b-versatile",
    "messages": [{"role": "user", "content": "halo"}],
    "max_tokens": 5 
}

print("Sedang mengecek limit ke server Groq...\n")
response = requests.post(URL, headers=headers, json=payload)

print(f"Status Code : {response.status_code}")
if response.status_code == 200:
    print("-" * 30)
    print("📊 STATUS RATE LIMIT GROQ ANDA:")
    print("-" * 30)
    print(f"Sisa Requests (RPM) : {response.headers.get('x-ratelimit-remaining-requests', 'N/A')} requests")
    print(f"Sisa Tokens (TPM)   : {response.headers.get('x-ratelimit-remaining-tokens', 'N/A')} tokens")
    print(f"Batas Limit (RPM)   : {response.headers.get('x-ratelimit-limit-requests', 'N/A')}")
else:
    print("Gagal mengecek. Error detail:", response.text)