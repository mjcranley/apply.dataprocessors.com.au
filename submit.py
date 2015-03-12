from selenium import webdriver
import sys
import signal

def signal_handler(signal, frame):
    print "Submission aborted"
    sys.exit(0)

def submission(URL, ref):
    signal.signal(signal.SIGINT, signal_handler)
    driver = webdriver.Firefox()
    driver.get(URL)
    html_source = driver.page_source
    ref_field = driver.find_element_by_xpath("/html/body/form/p[1]/input")
    ref_field.send_keys(ref)
    question = driver.find_element_by_xpath("/html/body/form/p[2]").text
    question = question.partition('Question: ')[2]
    question = question.replace(u' ',u'')
    answer = eval(question)
    answer_field = driver.find_element_by_xpath("/html/body/form/input[2]")
    answer_field.send_keys(answer)
    submit = driver.find_element_by_xpath("/html/body/form/p[4]/input")
    print "%s = %i" %(question, answer)
    response = submit.click()
    response_source = driver.page_source
    if driver.find_element_by_xpath("/html/body/p[1]").text == "Congratulations!":
        print "Congratulations! Refer to open Firefox window for instructions"
    else:
        driver.close()
        print "Submission Failed, attempting again - CTRL-C to abort"
        submission(URL, ref)

if __name__ == "__main__":
    submission('http://apply.dataprocessors.com.au/', 'PO29')
