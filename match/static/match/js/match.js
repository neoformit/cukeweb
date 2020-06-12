function validateTankSelect(select) {
    const value = $('form select').val();
    if (value != '') {
        validSelect()
    } else {
        invalidSelect()
    }
}

async function blurTargetsInput(input) {
    await new Promise((resolve) => setTimeout(resolve, 100));
    if ($('div.targets input').is(":focus")) {
        // User clicked on dropdown
        console.log('Blur target input: focus returned to input.')
        return
    }
    console.log('Blur target input: focus NOT returned to input.')
    input.value = '';
    $('div.targets .dropdown').empty();
    $('div.targets .dropdown').css('opacity', '0');
}

function resetForm() {
    $('div.targets .input').val('');
    $('div.targets .dropdown').empty();
    $('div.targets .selected').empty();
    invalidDropdown();
}

function validDropdown() {
    $('.tanks .dropdown').addClass('valid');
    $('.targets input').removeAttr('disabled');
    validateForm()
}

function invalidDropdown() {
    $('.tanks .dropdown').removeClass('valid');
    $('.targets input').prop('disabled', 'true');
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
    console.log('Invalid files selected');
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
        console.log('validateForm: form valididated')
        $('button:submit').removeAttr('disabled')
    } else {
        console.log('validateForm: form not valid')
        $('button:submit').prop('disabled', 'true')
    }
}
