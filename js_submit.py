from selenium import webdriver
import sys
import signal

URL = 'http://apply.dataprocessors.com.au/'
script = """
(function() {
    var script = document.createElement("SCRIPT");
    script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js';
    script.type = 'text/javascript';
    document.getElementsByTagName("head")[0].appendChild(script);

    // Poll for jQuery to come into existence
    var checkReady = function(callback) {
        if (window.jQuery) {
            callback(jQuery);
        }
        else {
            window.setTimeout(function() { checkReady(callback); }, 100);
        }
    };

    checkReady(function($) {
        question = $('*:contains("Question")');
        question = question.last();
        question = question.text();
        answer = eval(question.substring(question.indexOf(':')+1));
        input = $( "input[name='value']" )
        input.val(answer);
        jbref = $( "input[name='jobref']" )
        jbref.val('PO29');
        submt = $( "input[value='Submit']" )
        submt.click();
    });
})();"""

def signal_handler(signal, frame):
    print "Submission aborted"
    sys.exit(0)

def submission(URL):
    signal.signal(signal.SIGINT, signal_handler)
    driver = webdriver.Firefox()
    driver.get(URL)
    driver.execute_script(script)
    if driver.find_element_by_xpath("/html/body/p[1]").text == "Congratulations!":
        print "Congratulations! Refer to open Firefox window for instructions"
    else:
        driver.close()
        print "Submission Failed, attempting again - CTRL-C to abort"
        submission(URL)

if __name__ == "__main__":
    submission('http://apply.dataprocessors.com.au/')
