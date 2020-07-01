let globalNonse = new Object();

async function validateTankName(input) {
    // Clear select field
    resetSelect();

    // Set nonse to restrict event firing
    let localNonse = globalNonse = new Object();

    $('label.file-input').addClass('disabled');

    // If no characters
    if (!input.value) {
        resetInput();
        return
    }

    // If ID too short
    if (input.value.length < 4) {
        invalidInput('Must be 4 characters minimum');
        return
    }

    // Check nonse to see if user still typing
    await new Promise((resolve) => setTimeout(resolve, 500));
    if (!localNonse === globalNonse) { return }

    const tankName = input.value;

    // If tank exists
    if (existingTanks.includes(tankName)) {
        // Tank name found in registry.
        invalidInput('A tank with this ID already exists.');
    } else {
        // Tank name not in db. User is creating a new tank.
        validInput();
    }
}

function validateTankSelect(select) {
    if (select.selectedIndex) {
        validSelect();
    } else {
        invalidSelect();
    }
}

function validInput() {
    $('form.register-form-group .input-box').addClass('valid');
    $('form.register-form-group .input-box').removeClass('invalid');
    $('form.register-form-group .error-msg').empty();
    $('label.file-input').removeClass('disabled');
    $('input:file').removeAttr('disabled');
    validateForm()
}

function validSelect() {
    resetInput();
    $('form.register-form-group .dropdown').addClass('valid');
    $('label.file-input').removeClass('disabled');
    $('input:file').removeAttr('disabled');
    validateForm()
}

function invalidInput(msg) {
    $('form.register-form-group .input-box').removeClass('valid');
    $('form.register-form-group .input-box').addClass('invalid');
    $('form.register-form-group .error-msg').text(msg);
    $('label.file-input').addClass('disabled');
    $('input:file').prop('disabled', 'true');
    validateForm()
}

function invalidSelect() {
    $('form.register-form-group .dropdown').removeClass('valid');
    if (!$('form.register-form-group .input-box.valid').length) {
        $('label.file-input').addClass('disabled');
        $('input:file').prop('disabled', 'true');
    }
    validateForm()
}

function resetInput() {
    $('form.register-form-group .input-box input').val('');
    $('form.register-form-group .input-box').removeClass('valid');
    $('form.register-form-group .input-box').removeClass('invalid');
    $('form.register-form-group .error-msg').empty();
    $('label.file-input').addClass('disabled');
    $('input:file').prop('disabled', 'true');
    validateForm()
}

function resetSelect() {
    $('form.register-form-group select').val('');
    $('form.register-form-group .dropdown').removeClass('valid');
    $('form.register-form-group .dropdown').removeClass('invalid');
    $('form.register-form-group .error-msg').empty();
    $('label.file-input').addClass('disabled');
    $('input:file').prop('disabled', 'true');
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
    $('form.register-form-group .error-msg').empty();
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
    $('form.register-form-group .error-msg').text(
        'Must be either .jpg or .jpeg files!');
}

function validateForm() {
    if (
        ($('form.register-form-group .input-box').hasClass('valid')
         || $('form.register-form-group .dropdown').hasClass('valid'))
        & $('input:file').val() != ''
    ) {
        $('button:submit').removeAttr('disabled')
    } else {
        $('button:submit').prop('disabled', 'true')
    }
}

function formSubmit() {
    const new_tank = $('#tank_id')[0].value;
    const existing_tank = $('#tank_id_select')[0].value;

    if (!new_tank) {
        if (existingTanks.includes(existing_tank)) {
            $('#tank_id').val(existing_tank);
        } else {
            $('form.register-form-group .error-msg').text(
                'A tank identifier must be provided');
                return false
        }
    }
    // Add estimated time to loading overlay and fade in
    const n = $('input[type="file"]')[0].files.length;
    const time = Math.round(n * 2.8);
    $('#loading-animation span.num').text(n);
    $('#loading-animation span.time').text(time);
    $('#loading-animation').fadeIn(500);
    return true
}
