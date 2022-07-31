#!/bin/python
from time import sleep
from random import randint
from socket import gethostbyname
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome as Browser
from random_username.generate import generate_username


def page_element(find_by, element, action='', action_args='', timeout=30):
    page_element = ''
    while not page_element and timeout != 0:
        try:
            page_element = browser.find_element(find_by, element)
            if action:
                try:
                    if action_args:
                        getattr(page_element, action)(action_args)
                    else:
                        getattr(page_element, action)()
                    return True
                except Exception as error:
                    print(error)
            else:
                return page_element.text
        except Exception:
            sleep(1)
            timeout -= 1
    if timeout == 0:
        print('The waiting time for the element has expired:')
        print([find_by, element])
        return False


def write_data_to_file(file_path, data):
    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(data)
            print(f"The data is written to a file: '{file_path}'")
            return True
    except PermissionError:
        print('The operation is not allowed! Check read/write permissions:')
        print(file_path)
        return False


try:
    ssh_uri = 'https://opentunnel.net'
    print('Launching the browser', end=' ')
    browser = Browser(headless=True)
    print('[\u2713]')
    print('Opening a URI:', ssh_uri, end=' ')
    browser.get(ssh_uri)
    print('[\u2713]')
    print('Accepting cookies', end=' ')
    page_element(By.XPATH, "//button[@class='btn btn-outline-light w-100']", 'click')
    print('[\u2713]')
    print('Creating a list of SSH servers', end=' ')
    ssh_list = browser.find_elements(By.XPATH, "//a[@class='btn btn-outline-primary']")
    print('[\u2713]')
    print('Choosing a random SSH server', end=' ')
    browser.get(ssh_list[randint(1, len(ssh_list))].get_attribute('href'))
    print('[\u2713]')
    print('Generating SSH username', end=' ')
    ssh_username = generate_username()[0]
    print('[\u2713]')
    print('Generating SSH password', end=' ')
    ssh_password = generate_username()[0]
    print('[\u2713]')
    print('Creating an account...')
    page_element(By.XPATH, "//input[@name='username']", 'send_keys', ssh_username)
    page_element(By.XPATH, "//input[@name='password']", 'send_keys', ssh_password)
    page_element(By.XPATH, "//button[@class='btn btn-primary btn-sm w-100 subb']", 'click')
    ssh_info = page_element(By.XPATH, "//div[@class='alert alert-success text-left text account']")
    print('Formatting output data', end=' ')
    ssh_host = page_element(By.XPATH, "//li[@class='list-group-item py-2']").split()[1]
    ssh_ip = gethostbyname(ssh_host)
    ssh_info = '\n'.join(ssh_info.split('\n')[:-5][1:]).replace('Host To IP', ssh_ip).replace('How to use?', '')
    ssh_user = ssh_info.split('\n')[0].split()[1]
    print('[\u2713]')
    print('~' * 50)
    print('\nFree Premium SSH:')
    print(ssh_info + '\n')
    print('~' * 50)
    print('Connect to SSH:')
    print(f'# ssh -N -D 1080 {ssh_user}@{ssh_ip}')
    print('Configure the proxy server in your browser to 127.0.0.1:1080\n')
    write_data_to_file('ssh_info.txt', ssh_info + '\n\n')
except (KeyboardInterrupt, EOFError):
    browser.quit()
    quit()
finally:
    browser.quit()
    quit()
