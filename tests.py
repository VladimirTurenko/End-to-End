import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("headless")
    options.add_argument("window-size=1920x1080")
    driver = webdriver.Chrome()
    driver.maximize_window()
    start_url = "https://springboot-angular-shop.herokuapp.com/product"
    driver.get(start_url)
    yield driver
    driver.quit()

    # driver = webdriver.Edge()
    # start_url = "http://localhost/product"


# авторизованный пользователь может создать заказ
def test_main(driver):
    signin = driver.find_element(By.XPATH, "//a[contains(text(), 'Sign In')]")
    signin.click()

    login = driver.find_element(by=By.CSS_SELECTOR, value='#email')
    password = driver.find_element(by=By.CSS_SELECTOR, value='#password')
    login.send_keys('customer1@email.com')
    password.send_keys('123')

    signin_button = driver.find_element(by=By.XPATH, value='//button[text()="Sign In"]')
    signin_button.click()

    driver.implicitly_wait(20)

    get_it = WebDriverWait(driver, 20).until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, "//a[contains(text(), 'Get It')]")))
    get_it.click()

    driver.implicitly_wait(10)

    add_to_cart = driver.find_element(By.XPATH, "//button[contains(text(),'Add')]")
    add_to_cart.click()
    driver.implicitly_wait(10)

    checkout = driver.find_element(by=By.XPATH, value='//button[text()="Checkout"]')
    checkout.click()

    # checkout = driver.find_element(By.CSS_SELECTOR, 'body > app-root > div > app-cart > table > tbody > tr > td:nth-child(6) > a')
    # checkout.click()


#

# проверка названия сайта и главной страницы
def test_1(driver):
    text = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located(
            (By.TAG_NAME, 'h1'))).text
    assert 'Shop' in driver.title
    assert 'Get Whatever You Want!' in text


# негативный ввод логина и пароля
def test_2(driver):
    signin = driver.find_element(By.XPATH, "//a[contains(text(), 'Sign In')]")
    signin.click()

    login = driver.find_element(by=By.CSS_SELECTOR, value='#email')
    password = driver.find_element(by=By.CSS_SELECTOR, value='#password')
    login.send_keys('123')
    password.send_keys('123')

    signin_button = driver.find_element(by=By.XPATH, value='//button[text()="Sign In"]')
    signin_button.click()

    error = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, "//div[contains(text(), 'Invalid')]"))).text
    assert "Invalid username" in error


# позитивный ввод логин пароль
def test_3(driver):
    signin = driver.find_element(By.XPATH, "//a[contains(text(), 'Sign In')]")
    signin.click()

    login = driver.find_element(by=By.CSS_SELECTOR, value='#email')
    password = driver.find_element(by=By.CSS_SELECTOR, value='#password')
    login.send_keys('customer1@email.com')
    password.send_keys('123')

    signin_button = driver.find_element(by=By.XPATH, value='//button[text()="Sign In"]')
    signin_button.click()

    sign_out = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, "//a[contains(text(), 'Sign Out')]"))).text
    assert "Sign Out" in sign_out


# корректное перелистывание страниц
def test_4(driver):
    next_button = WebDriverWait(driver, 15).until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, '//a[text()="Next"]')))
    next_button.click()
    driver.implicitly_wait(20)
    driver.refresh()

    button_3 = WebDriverWait(driver, 20).until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, '//a[text()="3"]')))
    driver.implicitly_wait(20)
    button_3.click()

    button_4 = WebDriverWait(driver, 20).until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, '//a[text()="4"]')))
    driver.implicitly_wait(20)
    button_4.click()

    prev_button = WebDriverWait(driver, 20).until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, "//a[contains(text(), 'Prev')]")))
    driver.implicitly_wait(20)
    prev_button.click()


# корректный вывод subtotal при изменении кол-ва книг
def test_5(driver):
    get_book = driver.find_element(By.XPATH, "//a[contains(text(), 'Get It')]")
    get_book.click()
    driver.implicitly_wait(20)

    amount = driver.find_element(By.NAME, 'count')
    amount.clear()
    amount.send_keys(10)
    driver.implicitly_wait(5)

    text = WebDriverWait(driver, 15).until(
        expected_conditions.presence_of_element_located(
            (By.CSS_SELECTOR, '#subtotal'))).text
    assert '$300.00' in text


# пользователь не может купить без авторизации
def test_6(driver):
    book = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, "//a[contains(text(), 'Get It')]")))
    book.click()

    driver.implicitly_wait(10)
    add_to_cart = driver.find_element(By.XPATH, "//button[contains(text(),'Add')]")
    add_to_cart.click()

    total = driver.find_elements(By.TAG_NAME, 'td')
    assert '$30.00' in total[3].text

    checkout = driver.find_element(By.XPATH, "//button[contains(text(),'Checkout')]")
    checkout.click()

    signin = driver.find_element(By.TAG_NAME, 'h1').text
    assert 'Sign In' in signin


#
#
# корректное удаление из корзины
def test_7(driver):
    get_book = driver.find_element(By.XPATH, "//a[contains(text(), 'Get It')]")
    get_book.click()

    driver.implicitly_wait(10)
    add_to_cart = driver.find_element(By.XPATH, "//button[contains(text(),'Add')]")
    add_to_cart.click()

    total = driver.find_element(By.TAG_NAME, 'h5').text
    assert '$30.00' in total

    remove = driver.find_element(By.XPATH, "//a[contains(text(), 'Remove')]")
    remove.click()

    text = driver.find_element(By.TAG_NAME, 'h4').text
    assert 'Cart is empty. Go to get something! :)' in text


# авторизованному пользователю доступен просмотр заказов
def test_8(driver):
    signin = driver.find_element(By.XPATH, "//a[contains(text(), 'Sign In')]")
    signin.click()

    login = driver.find_element(by=By.CSS_SELECTOR, value='#email')
    password = driver.find_element(by=By.CSS_SELECTOR, value='#password')
    login.send_keys('customer1@email.com')
    password.send_keys('123')

    signin_button = driver.find_element(by=By.XPATH, value='//button[text()="Sign In"]')
    signin_button.click()
    driver.implicitly_wait(5)

    orders = driver.find_element(By.XPATH, "//a[contains(text(), 'Orders')]")
    orders.click()
    #
    orders = WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located(
            (By.TAG_NAME, 'h1'))).text
    assert 'Orders' in orders


# авторизованному пользователю доступно изменение личной информации
def test_9(driver):
    signin = driver.find_element(By.XPATH, "//a[contains(text(), 'Sign In')]")
    signin.click()

    login = driver.find_element(by=By.CSS_SELECTOR, value='#email')
    password = driver.find_element(by=By.CSS_SELECTOR, value='#password')
    login.send_keys('customer1@email.com')
    password.send_keys('123')

    signin_button = driver.find_element(by=By.XPATH, value='//button[text()="Sign In"]')
    signin_button.click()

    driver.implicitly_wait(5)
    change_info = driver.find_element(By.CSS_SELECTOR, '#navbarNav > div.navbar-nav.ml-auto > a:nth-child(3)')
    change_info.click()

    b = driver.find_elements(By.TAG_NAME, 'b')
    assert 'Email address' in b[0].text
    # assert 'Name' in b[1].text
    # assert 'Password' in b[2].text


# пользователь не может добавить в корзину больше товара, чем есть на складе
def test_10(driver):
    book_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Get It')]")
    book_button.click()

    quantity = driver.find_element(By.NAME, 'count')
    quantity.send_keys('00')
    driver.implicitly_wait(5)

    add_to_cart = driver.find_element(By.XPATH, "//button[contains(text(), 'Add')]")
    add_to_cart.click()

    subtotal = driver.find_elements(By.TAG_NAME, 'td')
    assert '$2,520.00' in subtotal[3].text


# администратору доступно изменение товаров
def test_11(driver):
    signin = driver.find_element(By.XPATH, "//a[contains(text(), 'Sign In')]")
    signin.click()

    login = driver.find_element(by=By.CSS_SELECTOR, value='#email')
    password = driver.find_element(by=By.CSS_SELECTOR, value='#password')
    login.send_keys('manager1@email.com')
    password.send_keys('123')

    signin_button = driver.find_element(by=By.XPATH, value='//button[text()="Sign In"]')
    signin_button.click()

    driver.implicitly_wait(10)

    edit = driver.find_element(By.XPATH, "//a[contains(text(), 'Edit')]")
    edit.click()

    title = WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located(
            (By.CSS_SELECTOR, 'h1'))).text
    assert "Edit Product" in title


# администратор может просматривать заказы пользователей
def test_12(driver):
    signin = driver.find_element(By.XPATH, "//a[contains(text(), 'Sign In')]")
    signin.click()

    login = driver.find_element(By.CSS_SELECTOR, '#email')
    password = driver.find_element(By.CSS_SELECTOR, '#password')
    login.send_keys('manager1@email.com')
    password.send_keys('123')

    signin_button = driver.find_element(By.XPATH, '//button[text()="Sign In"]')
    signin_button.click()

    driver.implicitly_wait(10)
    orders = driver.find_element(By.XPATH, "//a[contains(text(), 'Orders')]")
    orders.click()

    show = driver.find_element(By.XPATH, "//a[contains(text(), 'Show')]")
    show.click()

    title = WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located(
            (By.CSS_SELECTOR, 'h1'))).text
    assert "Order Detail" in title


# пользователь не может зарегистрироваться, если такая почта уже есть в базе
def test_13(driver):
    ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)

    signup = driver.find_element(By.XPATH, "//a[contains(text(), 'Sign Up')]")
    signup.click()

    email = driver.find_element(By.CSS_SELECTOR, '#email')
    name = driver.find_element(By.CSS_SELECTOR, '#name')
    psw = driver.find_element(By.CSS_SELECTOR, '#password')
    phone = driver.find_element(By.CSS_SELECTOR, '#phone')
    address = driver.find_element(By.CSS_SELECTOR, '#address')

    email.send_keys('customer1@email.com')
    name.send_keys('1')
    psw.send_keys('433')
    phone.send_keys('1')
    address.send_keys('123')

    signup_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign Up')]")
    signup_button.click()

    title = WebDriverWait(driver, 5, ignored_exceptions=ignored_exceptions).until(
        expected_conditions.presence_of_element_located(
            (By.CSS_SELECTOR, 'h1'))).text
    assert "Sign Up" in title


def test_14(driver):
   books = driver.find_element_by_xpath("//a[contains(text(), 'Books')]")
    books.click()

    driver.implicitly_wait(10)
    unavailable_button = driver.find_element(by=By.CSS_SELECTOR, value='body > app-root > div > app-card > div > '
                                                                       'div:nth-child(3) > div > div')
    unavailable_button.click()

    title = driver.find_element(By.CSS_SELECTOR, 'h1').text
    assert 'Books' in title


def main():
    test_14(driver)
    test_13(driver)
    test_12(driver)
    test_11(driver)
    test_10(driver)
    test_9(driver)
    test_8(driver)
    test_7(driver)
    test_6(driver)
    test_5(driver)
    test_3(driver)
    test_2(driver)
    test_1(driver)
    test_4(driver)
    test_main(driver)


if __name__ == "__main__":
    main()
