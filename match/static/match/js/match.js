function validateTank(tank_id) {
    const value = $('form select').val();
    if (value != '') {
        selectTank(tank_id)
    } else {
        invalidTankSelection()
    }
}

async function blurTargetsInput(input) {
    await new Promise((resolve) => setTimeout(resolve, 100));
    if ($('div.targets input').is(":focus")) {
        // User clicked on dropdown
        return
    }
    input.value = '';
    $('div.targets .dropdown').empty();
    $('div.targets .dropdown').css('opacity', '0');
}

function resetForm() {
    $('div.targets .input').val('');
    $('div.targets .dropdown').empty();
    $('div.targets .selected').empty();
    invalidTankSelection();
}

function validTankSelection() {
    $('.tanks .dropdown').addClass('valid');
    $('.file-input').removeClass('disabled');
    $('input').removeAttr('disabled');
    validateForm()
}

function invalidTankSelection() {
    $('.tanks .dropdown').removeClass('valid');
    $('.file-input').addClass('disabled');
    $('input').prop('disabled', 'true');
    validateForm()
}

function validateFiles(input) {
    const n = input.files.length;
    for (var i = 0; i < n; ++i) {
        let file = input.files[i];
        if (!(file.name.endsWith('.jpg') || file.name.endsWith('.jpeg'))) {
            invalidFiles();
            validateForm();
            return
        }
    }
    validFiles(n);
    validateForm();
}

function validFiles(n) {
    $('.error-msg').empty();
    if (n === 1) {
        $('#fileCount').text('1 file selected')
    }
    $('#fileCount').text(n + ' files selected')
    $('label.file-input').addClass('valid');
}

function invalidFiles() {
    $('input:file').val('');
    $('label.file-input').removeClass('valid');
    $('#fileCount').text('0 files selected')
    $('form.match-form-group .error-msg').text('Must be either .jpg or .jpeg files!');
}

function validateForm() {
    if (
        ($('.tanks .dropdown').hasClass('valid'))
        & $('input:file').val() != ''
    ) {
        $('button:submit').removeAttr('disabled')
    } else {
        $('button:submit').prop('disabled', 'true')
    }
}

function submitAnimate() {
    const n_query = $('input[type="file"]')[0].files.length;
    const n_subject = targetIds.length;
    const time = Math.round(n_query * n_subject * 1.2354);
    $('#loading-animation span.queries').text(n_query);
    $('#loading-animation span.subjects').text(n_subject);
    $('#loading-animation span.time').text(time);
    $('#loading-animation').fadeIn(500);
}
