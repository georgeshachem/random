from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException

matricule = "INSERT-MATRICULE-HERE"
password = "INSERT-PASSWORD-HERE"

project_number = "X"

text_to_send = "Je soussigné FIRST1 LAST1 (TR) certifie avoir obtenu l’accord des personnes suivantes : FIRST2 LAST2 (TR), FIRST3 LAST3 (GL), FIRST4 LAST4 (GL) pour demander l’attribution du projet {}. Nous satisfaisons les effectifs demandés dans le sujet.".format(project_number)

cour = "020PRMES4 - Projet multidisciplinaire"
forum = "Sélection des projets"
topic = "Choix du sujet {}".format(project_number)


def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return True
    return False


def mdp_bot(username, password):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://moodle.usj.edu.lb/login/index.php")

    driver.find_element_by_id('username').send_keys(username)
    driver.find_element_by_id('password').send_keys(password)

    driver.find_element_by_id('loginbtn').click()

    driver.find_element_by_xpath('//a[text()="{}"]'.format(cour)).click()
    while check_exists_by_xpath(driver, '//span[text()="{}"]'.format(forum)):
        driver.refresh()
    driver.find_element_by_xpath('//span[text()="{}"]'.format(forum)).click()
    sujets = driver.find_elements_by_xpath("//div[@class='forumpost clearfix firstpost starter']")
    for sujet in sujets:
        if topic in sujet.get_attribute("aria-label"):
            sujet.find_element_by_xpath(".//a[text()='Discuter sur ce sujet']").click()
            break
    driver.find_element_by_xpath("//a[text()='Répondre']").click()
    time.sleep(5)
    script_to_execute = "window.parent.tinyMCE.activeEditor.setContent('{}')".format(text_to_send)
    driver.execute_script(script_to_execute)

    driver.find_element_by_xpath("//input[@id='id_submitbutton']").click()


if __name__ == '__main__':
    mdp_bot(matricule, password)
