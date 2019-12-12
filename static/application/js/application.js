function phone_formatting(ele, restore) {
  let new_number,
    selection_start = ele.selectionStart,
    selection_end = ele.selectionEnd,
    number = ele.value.replace(/\D/g, '');

  // automatically add dashes
  if (number.length > 2) {
    // matches: 123 || 123-4 || 123-45
    new_number = '(' + number.substring(0, 3) + ') ';
    if (number.length === 4 || number.length === 5) {
      // matches: 123-4 || 123-45
      new_number += number.substr(3);
    } else if (number.length > 5) {
      // matches: 123-456 || 123-456-7 || 123-456-789
      new_number += number.substring(3, 6) + '-';
    }
    if (number.length > 6) {
      // matches: 123-456-7 || 123-456-789 || 123-456-7890
      new_number += number.substring(6);
    }
  } else {
    new_number = number;
  }

  // if value is higher than 12, last number is dropped
  // if inserting a number before the last character, numbers
  // are shifted right, only 12 characters will show
  ele.value = (new_number.length > 14) ? new_number.substring(0, 14) : new_number;

  // restore cursor selection,
  // prevent it from going to the end
  // UNLESS
  // cursor was at the end AND a dash was added

  if (new_number.slice(-1) === '-' && restore === false &&
    (new_number.length === 8 && selection_end === 7) ||
    (new_number.length === 4 && selection_end === 3)) {
    selection_start = new_number.length;
    selection_end = new_number.length;
  } else if (restore === 'revert') {
    selection_start--;
    selection_end--;
  }
  ele.setSelectionRange(selection_start, selection_end);
}

function phone_number_check(field, e) {
    let key_code = e.keyCode,
    key_string = String.fromCharCode(key_code),
    press_delete = false,
    dash_key = 189,
    delete_key = [8, 46],
    direction_key = [33, 34, 35, 36, 37, 38, 39, 40],
    selection_end = field.selectionEnd;

  // delete key was pressed
  if (delete_key.indexOf(key_code) > -1) {
    press_delete = true;
  }

  // only force formatting is a number or delete key was pressed
  if (key_string.match(/^\d+$/) || press_delete) {
    phone_formatting(field, press_delete);
  }
  // do nothing for direction keys, keep their default actions
  else if (direction_key.indexOf(key_code) > -1) {
    // do nothing
  } else if (dash_key === key_code) {
    if (selection_end === field.value.length) {
      field.value = field.value.slice(0, -1)
    } else {
      field.value = field.value.substring(0, (selection_end - 1)) + field.value.substr(selection_end)
      field.selectionEnd = selection_end - 1;
    }
  }
  // all other non numerical key presses, remove their value
  else {
    e.preventDefault();
    //    field.value = field.value.replace(/[^0-9\-]/g,'')
    phone_formatting(field, 'revert');
  }
}

$(document).ready(function () {

    // This is used to load programs for selected school
    let k;
    for (k = 0; k < 10; k++) {
        if($('#school' + k).children('option:selected').val() == "") {
            $('#program' + k).html("<option value=\"\" selected>---------</option>");
        }

        $('#school' + k).on('change', function() {
            let id = this.id.substring(6);
            let url = $('form').attr('prog-data-url');
            let school_id = $(this).children('option:selected').val();

            let prog = [];
            let j;
            for (j = 0; j < 10; j++) {
                let sid = $('#school' + j).children('option:selected').val();
                if (j != id && sid == school_id) {
                    let pid = $('#program' + j).children('option:selected').val();
                    if (pid) {
                        prog.push(pid);
                    }
                }
            }

            let program_input = $('#program' + id);

            $.ajax({
                url: url,
                data: {
                    'selected_school_id': school_id,
                    'prog': JSON.stringify(prog)
                },
                type: 'POST',
                    success: function(data) {
                        $(program_input).html(data);
                    },
                traditional: true,
            });
        });
    }

    $('#addBtn').on('click', function() {
         let i;
         for (i = 0; i <= 10; i++) {
             if(i == 10) {
                alert("You can apply to maximum 10 schools.");
             }
             else if ($('#school' + i + 'div').css('display') == 'none') {
                 $('#school' + i + 'div').css('display', 'block');
                 $('#program' + i + 'div').css('display', 'block');
                 $('#select2-school' + i + '-container').html('---------');
                 $('#school' + i).prop('required', true);
                 $('#program' + i).prop('required', true);
                 break;
            }
         }
    });

    $('#rmBtn').on('click', function() {
         let i;
         for (i = 9; i >= 0; i--) {
             if(i == 0) {
                 alert("Atleast one school and program is required to complete application");
             }
             else if ($('#school' + i + 'div').css('display') == 'block') {
                 $('#school' + i + 'div').css('display', 'none');
                 $('#program' + i + 'div').css('display', 'none');
                 $('#select2-school' + i + '-container').html('---------');
                 $('#program' + i).prop('selectedIndex', 0);
                 $('#school' + i).prop('required', false);
                 $('#program' + i).prop('required', false);
                 break;
             }
         }
    });

     $('#phoneNumber').on('keyup', function(e) {
        phone_number_check(this, e);
        $(this).focus();
        this.setSelectionRange(this.value.length, this.value.length);
    });

    $('#parent_phoneNumber').on('keyup', function(e) {
        phone_number_check(this, e);
        $(this).focus();
        this.setSelectionRange(this.value.length, this.value.length);
    });

});