from selenium import webdriver

driver = webdriver.Firefox()
URL = 'http://apply.dataprocessors.com.au/'
driver.get(URL)
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
driver.execute_script(script)
response = str(raw_input("Was submission successful? [y/n]: "))
if response in {'Y', 'y', 'Yes', 'yes', ''}:
    print "Congratulations! Refer to open Firefox window for instructions"
elif response in {'N', 'n', 'No', 'no'}:
    retry = str(raw_input("Would you like to try again? [y/n]: "))
    if retry in {'Y', 'y', 'Yes', 'yes', ''}:
        driver.close()
        driver.get(URL)
        driver.execute(script)
    elif retry in {'N', 'n', 'No', 'no'}:
        print "Submission Failed"
    else:
        print "Not an accepted answer, Submission Failed"
else:
    print "Not an accepted answer, Submission Failed"
    driver.close()

