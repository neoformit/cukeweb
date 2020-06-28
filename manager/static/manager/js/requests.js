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
            $(`#${ tank_id }`).remove();
            closeModal();
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
            $(`#${ tank_id } #${ cuke_id }`).remove();
            closeModal();
        },
        error: function(xhr, status, msg) {
            newTabErrorMessage(xhr);
        }
    });
}


function updateCukeRequest() {
    // Retrieve values from modal form
    const tank_id = $('.modal.edit span.tank_id').text();
    const cuke_id = $('.modal.edit span.cuke_id').text();
    const detailDivs = $('form div.detail');
    let details = {};
    // Collect only detail fields which have been updated
    detailDivs.each( function(i, item) {
        let key = $(item).children('input')[0].value;
        let oldKey = $(item).children('input')[0].placeholder;
        let value = $(item).children('input')[1].value;
        let oldVal = $(item).children('input')[1].placeholder;
        if (key === oldKey & value === oldVal) { return }
        details[oldKey] = {'key': key, 'value': value}
    });

    let key = $('form input[name="new_key"]')[0].value;
    let value = $('form input[name="new_value"]')[0].value;
    if (key && value) {
        details[key] = {'key': key, 'value': value};
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
