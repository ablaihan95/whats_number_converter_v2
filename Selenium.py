from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def parser(text: str):
    krishatype = "web"
    if text.__contains__("//m."):
        krishatype = "mobile"

    options = Options()
    options.headless = True
    driver: WebDriver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    arr: str = []
    try:
        driver.get(text)

        if krishatype.__eq__("web"):
            WebDriverWait(driver, timeout=5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".show-phones")))
            driver.find_element(By.CSS_SELECTOR, ".show-phones").click()
            WebDriverWait(driver, timeout=5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".offer__contacts-phones p")))
            tns = driver.find_elements(By.CSS_SELECTOR, ".offer__contacts-phones p")
            for tel in tns:
                arr.append(tel.text)
            print(arr)
        else:
            submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Позвонить')]")
            WebDriverWait(driver, timeout=5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Позвонить')]")))

            submit_button.click()

            el = driver.find_element(By.CSS_SELECTOR, ".phones-modal__items")
            WebDriverWait(driver, timeout=5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".phones-modal__items a")))

            print(el.find_element(By.TAG_NAME, "a").is_displayed())
            tns = el.find_elements(By.TAG_NAME, "a")

            for tel in tns:
                arr.append(tel.find_element(By.TAG_NAME, "span").text)
            print(arr)
    except:
        arr.append("что пошло не так проверьте правильность сслыки")
    finally:
        driver.quit()
    return arr
