from bs4 import BeautifulSoup
import requests, csv, math
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import pandas as pd
import os

data_set = pd.read_csv("PhiUSIIL_Phishing_URL_Dataset.csv")
urls = data_set["URL"].head(20000).tolist()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}

def shannon_entropy(s):
    if not s:
        return 0
    prob = [float(s.count(c)) / len(s) for c in dict.fromkeys(list(s))]
    return round(-sum(p * math.log(p, 2) for p in prob), 3)

def fetch_url(url):
    try:
        res = requests.get(url, headers=headers, timeout=10, verify=False)
        html = res.text
        soup = BeautifulSoup(html, "html.parser")
        domain = urlparse(url).netloc.lower()
        text = soup.get_text(separator=" ", strip=True).lower()

        features = {"url": url}
        meta_refresh = [m for m in soup.find_all("meta") if m.get("http-equiv", "").lower() == "refresh"]
        features["meta_refresh_redirect"] = int(bool(meta_refresh))
        inline_scripts = [s.get_text() for s in soup.find_all("script") if not s.get("src") and s.get_text()]
        entropies = [shannon_entropy(js) for js in inline_scripts if js.strip()]
        features["script_entropy_avg"] = round(sum(entropies) / len(entropies), 3) if entropies else 0
        total_scripts = len(soup.find_all("script"))
        inline_count = len(inline_scripts)
        features["inline_script_ratio"] = round(inline_count / total_scripts, 3) if total_scripts else 0
        suspicious_words = ["login", "verify", "account", "bank", "password", "secure", "update", "confirm", "signin"]
        keyword_count = sum(text.count(w) for w in suspicious_words)
        total_words = len(text.split())
        features["suspicious_keyword_density"] = round(keyword_count / (total_words + 1e-5), 5)
        css_links = soup.find_all("link", rel=lambda v: v and "stylesheet" in v.lower())
        
        ext_css = 0
        for c in css_links:
            href = c.get("href")
            if href:
                full = urljoin(url, href)
                if urlparse(full).netloc and urlparse(full).netloc != domain:
                    ext_css += 1
        features["css_external_ratio"] = round(ext_css / (len(css_links) or 1), 3)

        base = soup.find("base", href=True)
        features["base_tag_mismatch"] = 0
        if base:
            base_domain = urlparse(urljoin(url, base["href"])).netloc.lower()
            if base_domain and base_domain != domain:
                features["base_tag_mismatch"] = 1

        title = (soup.title.string or "").lower() if soup.title else ""
        brand_terms = [d for d in domain.replace(".", " ").split() if len(d) > 2]
        mismatch = all(b not in title for b in brand_terms)
        features["title_brand_mismatch"] = int(mismatch and bool(title))

        imgs = soup.find_all("img")
        imgs_missing_alt = [img for img in imgs if not img.get("alt")]
        features["image_alt_anomaly_ratio"] = round(len(imgs_missing_alt) / (len(imgs) or 1), 3)

        return features

    except requests.exceptions.RequestException as e:
        print(f"[Error fetching {url}]: {e}")

def process_batch(batch_urls, batch_index):
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(fetch_url, url): url for url in batch_urls}

        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result(timeout=30) 
                if data:
                    results.append(data)
            except requests.exceptions.Timeout:
                print(f"[Skipped {url}] due to: Timeout after 30s")
            except Exception as e:
                print(f"[Error fetching {url}]: {e}")
                continue
    if results:
        out_file = f"html_features_batch_{batch_index}.csv"
        fieldnames = results[0].keys()
        with open(out_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"[✔] Batch {batch_index}: Saved {len(results)} pages → {out_file}")

if __name__ == "__main__":
    batch_size = 500
    total_batches = (len(urls) + batch_size - 1) // batch_size

    completed_batches = {
        int(f.split("_")[-1].split(".")[0])
        for f in os.listdir(".")
        if f.startswith("html_features_batch_") and f.endswith(".csv")
    }

    for i in range(total_batches):
        batch_num = i + 1
        # if batch_num == 33:
        #     batch_num += 4
        if batch_num in completed_batches:
            print(f"[Skipping batch] {batch_num} — already processed.")
            continue 

        start = i * batch_size
        end = min(start + batch_size, len(urls))
        batch_urls = urls[start:end]
        if not batch_urls:
            break

        print(f"\n[→] Processing batch {batch_num}/{total_batches} ({len(batch_urls)} URLs)...")
        process_batch(batch_urls, batch_num)
        time.sleep(2)
