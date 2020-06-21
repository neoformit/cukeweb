// Send request to email page link to given address

// Bind enter key to sendEmail
$('div.email').on('keypress', 'input', function(args) {
    if (args.keyCode == 13) {
        sendEmail($('div.email input')[0].value);
        return false;
    }
});

function emailForm() {
    $('div.email-overlay').fadeIn(500);
    $('div.email').removeClass('offscreen');
    $('div.email input').focus();
}

function sendEmail(address) {
    if (!is_email(address)) {
        return invalidEmail();
    }

    $('div.email .spinner').fadeIn(250);

    $.ajax({
        url : "/match/sendmail/",   // the endpoint
        type : "POST",              // http method
        data : {
            'address': address,
            'result_id': result_id,
        },

        // handle a successful response
        success : function(json) {
            emailSuccess();
        },
        error: function(xhr, status, msg) {
            // Say 'bad'
            hideEmailForm();
            // alert("Sorry, an error occurred sending email")
            newTabErrorMessage(xhr);
        }
    });
}

function is_email(address){
    const emailReg = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    return emailReg.test(address);
}

function invalidEmail() {
    $('div.email p.error-msg').text('Invalid email address')
}

function resetEmailForm() {
    $('div.email input').val('');
    $('div.email .spinner').hide();
    $('div.email .success').hide();
    $('div.email p.error-msg').text('');
    $('div.email button').show();
}

function hideEmailForm() {
    resetEmailForm();
    $('div.email').addClass('offscreen');
    $('div.email-overlay').fadeOut(500);
}

async function emailSuccess() {
    $('div.email .spinner').fadeOut(250);
    $('div.email button').hide();
    $('div.email .success').fadeIn(250);
    await new Promise((resolve) => setTimeout(resolve, 1500));
    resetEmailForm();
    hideEmailForm();
}

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}
