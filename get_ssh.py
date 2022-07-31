#!/bin/python
from time import sleep
from socket import gethostbyname
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome as Browser


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
    print(f"Opening a URI: '{ssh_uri}'", end=' ')
    browser.get(ssh_uri)
    print('[\u2713]')
    print('Accepting cookies', end=' ')
    page_element(By.XPATH, "//button[@class='btn btn-outline-light w-100']", 'click')
    print('[\u2713]')
    print('Creating a list of SSH servers...\n')
    all_ssh_list = browser.find_elements(By.XPATH, "//div[@class='my-2 p-2 bg-white rounded shadow-sm']")
    ssh_list = {}
    ssh_num = 1
    for ssh in all_ssh_list:
        try:
            ssh_list[str(ssh_num)] = ssh.find_element(By.XPATH, ".//a[@class='btn btn-outline-primary']")
            cur_ssh = ssh.text.replace('\nCreate', '').replace('SSH SSL', '\nSSH SSL').\
                replace('Squid', '\nSquid').replace('CF Host', '\nCF Host').\
                replace('DNS Host', '\nDNS Host').replace('SSH Server ', '').replace('\n', '\n   ')
            print(f'{ssh_num}. {cur_ssh}\n')
            ssh_num += 1
        except Exception:
            pass
    while not (ssh_choice := ssh_list.get(input('Select the server: '))):
        pass
    print('Opening an SSH server', end=' ')
    browser.get(ssh_choice.get_attribute('href'))
    print('[\u2713]')
    while not (ssh_username := input('Enter the user name: ')):
        pass
    page_element(By.XPATH, "//input[@name='username']", 'send_keys', ssh_username)
    while not (ssh_password := input('Enter the password: ')):
        pass
    page_element(By.XPATH, "//input[@name='password']", 'send_keys', ssh_password)
    print('Creating an account...')
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
