// Async requests for tank and cucumber management
function deleteTankRequest(tank_id) {
    // Make ajax request to delete tank
    $.ajax({
        url : "/manage/delete_tank/",   // the endpoint
        type : "POST",                  // http method
        data : {
            'tank_id': tank_id,
        },
        // handle a successful response
        success : function() {
            $(`#tank_${ tank_id }`).remove();
            $(`#row_${ tank_id }`).remove();
            closeModal();
            if (!$('div.tank').length) {
                location.reload();
            }
        },
        error: function(xhr, status, msg) {
            newTabErrorMessage(xhr);
        }
    });
}


function deleteCukeRequest(tank_id, cuke_id) {
    // Make ajax request to delete cucumber
    $.ajax({
        url : "/manage/delete_cuke/",   // the endpoint
        type : "POST",                  // http method
        data : {
            tank_id: tank_id,
            cuke_id: cuke_id,
        },
        // handle a successful response
        success : function() {
            $(`#tank_${ tank_id } #cuke_${ cuke_id }`).remove();
            let count = parseInt($(`#row_${ tank_id } span.count`).text());
            $(`#row_${ tank_id } span.count`).text(count - 1);
            closeModal();
        },
        error: function(xhr, status, msg) {
            newTabErrorMessage(xhr);
        }
    });
}


function updateCukeRequest() {
    if (!validateCukeUpdate()) { return }

    // Retrieve values from modal form
    const tank_id = $('.modal.edit span.tank_id').text();
    const cuke_id = $('.modal.edit span.cuke_id').text();
    const detailDivs = $('form div.detail');
    let details = {};
    let oldKey; let oldVal; let key; let value;

    // Collect only detail fields which have been updated
    detailDivs.each( function(i, item) {
        if (!item.innerHTML) {
            // Field was deleted
            oldKey = item.id;
            details[oldKey] = null;
            console.log(`updateCukeRequest: Field ${ oldKey } was deleted`);
            return
        }
        oldKey = $(item).children('input')[0].placeholder;
        oldVal = $(item).children('input')[1].placeholder;
        key = $(item).children('input')[0].value;
        value = $(item).children('input')[1].value;
        if (key === oldKey & value === oldVal) {
            // Field was not altered
            return
        }
        details[oldKey] = {'key': key, 'value': value}
        console.log(`updateCukeRequest: Field ${ oldKey } was collected for update request`);
    });

    key = $('form input[name="new_key"]')[0].value;
    value = $('form input[name="new_value"]')[0].value;
    if (key && value) {
        details[key] = {'key': key, 'value': value};
        console.log(`updateCukeRequest: Field ${ key } was created`);
    }

    if (!Object.keys(details).length) {
        console.log('No details to update. Request aborted.');
        return
    }

    // Make ajax request to update cucumber
    $.ajax({
        url : "/manage/update_cuke/",   // the endpoint
        type : "POST",                  // http method
        data : {
            tank_id: tank_id,
            cuke_id: cuke_id,
            details: JSON.stringify(details),
        },
        // handle a successful response
        success : function(json) {
            updateCukeDiv(tank_id, cuke_id, json);
            closeModal();
        },
        error: function(xhr, status, msg) {
            newTabErrorMessage(xhr);
        }
    });
}
