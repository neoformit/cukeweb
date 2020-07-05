// Functions for tank and cucumber management
function notifyAdminDialog(filename) {
    console.log(`Showing notify admin modal for filename "${ filename }"`);
    $('#notifyAdminModal button[type="submit"]').click(function() {
        notifyAdminRequest(`${ filename }`)
    });
    $('.modal-overlay').fadeIn(250);
    $('#notifyAdminModal').fadeIn(250);
}

async function closeModal() {
    $('.modal-overlay').fadeOut(250);
    $('.modal').fadeOut(250);
    await new Promise(r => (setTimeout(r, 1000)));
    resetModals();
}

function resetModals() {
    $('.modal img').hide();
    $('.modal .success').hide();
    $('.modal .dialog').show();
    $('.modal button.warn').unbind();
    $('.modal textarea').val('');
}

async function notifySuccess() {
    $('.modal img').hide();
    $('.modal .success').show();
    await new Promise(r => (setTimeout(r, 1500)));
    closeModal();
}

// Async requests for tank and cucumber management
function notifyAdminRequest(filename) {
    console.log(`Triggered report request for filename "${ filename }"`);
    // Animate load
    $('.modal .dialog').hide();
    $('.modal img').fadeIn(500);

    // Make ajax request to delete tank
    $.ajax({
        url : "/register/notify/",    // the endpoint
        type : "POST",                // http method
        data : {
            'filename': filename,
            'message': $('.modal textarea').val(),
        },
        // handle a successful response
        success : function() {
            notifySuccess()
        },
        error: function(xhr, status, msg) {
            closeModal();
            // alert("Server error")
            newTabErrorMessage(xhr); // For debugging only
        }
    });
}
