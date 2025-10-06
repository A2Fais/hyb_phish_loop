from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from dom_content_crawler_script import *

def create_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(30)
    return driver

def analyze_page(url):
    driver = create_driver()
    try:
        load_page(driver, url)
        results = {
            "dom_max_depth": dom_max_depth(driver),
            "dom_total_nodes": dom_total_nodes(driver),
            "dom_avg_branching_factor": dom_avg_branching_factor(driver),
            "dom_max_children_per_node": dom_max_children_per_node(driver),
            "dom_iframe_count": dom_iframe_count(driver),
            "dom_iframe_max_nesting": dom_iframe_max_nesting(driver),
            "dom_form_count": dom_form_count(driver),
            "dom_hidden_input_count": dom_hidden_input_count(driver),
            "dom_forms_external_action_ratio": dom_forms_external_action_ratio(driver),
            "dom_script_count": dom_script_count(driver),
            "dom_suspicious_script_count": dom_suspicious_script_count(driver),
            "dom_popup_indicators": dom_popup_indicators(driver),
            "dom_hover_url_mismatch_count": dom_hover_url_mismatch_count(driver),
            "dom_mixed_content_count": dom_mixed_content_count(driver),
            "dom_external_resource_count": dom_external_resource_count(driver),
            "dom_cross_origin_iframe_count": dom_cross_origin_iframe_count(driver),
            "dom_hidden_element_ratio": dom_hidden_element_ratio(driver),
            "dom_clickable_without_href_count": dom_clickable_without_href_count(driver),
            "dom_keyboard_event_on_password_count": dom_keyboard_event_on_password_count(driver),
            "dom_autocomplete_off_password_count": dom_autocomplete_off_password_count(driver),
            "dom_setTimeout_or_setInterval_presence": dom_setTimeout_or_setInterval_presence(driver),
            "dom_mutation_observer_presence": dom_mutation_observer_presence(driver),
            "dom_service_worker_register_presence": dom_service_worker_register_presence(driver),
            "dom_clipboard_access_presence": dom_clipboard_access_presence(driver),
            "dom_download_link_count": dom_download_link_count(driver),
            "dom_data_uri_image_count": dom_data_uri_image_count(driver),
            "dom_form_target_blank_count": dom_form_target_blank_count(driver),
            "dom_anchor_noopener_missing_ratio": dom_anchor_noopener_missing_ratio(driver),
            "dom_event_handler_attr_total": dom_event_handler_attr_total(driver),
            "dom_third_party_domains_unique": dom_third_party_domains_unique(driver),
        }
        return results
    finally:
        driver.quit()


if __name__ == "__main__":
    url = "https://www.wikipedia.org"
    features = analyze_page(url)
    for k, v in features.items():
        print(f"{k}: {v}")
