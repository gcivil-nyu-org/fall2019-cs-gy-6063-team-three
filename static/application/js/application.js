$(document).ready(function () {

    // This is used to load programs for selected school
    let k;
    for (k = 0; k < 10; k++) {
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
                 $('#select2-school' + i + '-container').empty();
                 $('#program' + i).prop('selectedIndex', 0)
                 break;
             }
         }
    });

    });