function validate() {
            console.log("In validate");
            let gpa_min = document.forms["filter_form"]["gpa_min"].value.trim();
            let gpa_max = document.forms["filter_form"]["gpa_max"].value.trim();

            let err_field = document.getElementById("gpa_error");
            let err_msg = "GPA value must be a number between 0 and 4";
            // If both are empty, ignore validation
            if (gpa_min === "" && gpa_max === "") {
                return true;
            }
            // If either one is non-empty and has a non-number, throw error
            if ((gpa_min !== "" && isNaN(gpa_min)) || (gpa_max !== "" && isNaN(gpa_max))) {
                show_err(err_field, err_msg);
                return false;
            }
            let gpa_min_number = NaN;
            let gpa_max_number = NaN;

            //  Check GPA min conditions
            if (gpa_min !== "" && !isNaN(gpa_min)) {
                gpa_min_number = Number(gpa_min);
                if (gpa_min_number < 0 || gpa_min_number > 4) {
                    show_err(err_field, err_msg);
                    return false;
                }
            }
            // Check GPA max conditions
            if (gpa_max !== "" && !isNaN(gpa_max)) {
                gpa_max_number = Number(gpa_max);
                if (gpa_max_number < 0 || gpa_max_number > 4) {
                    show_err(err_field, err_msg);
                    return false;
                }
            }
            // If min value is specified and max is not, set max to 4.
            if (!isNaN(gpa_min_number) && isNaN(gpa_max_number)) {
                document.forms["filter_form"]["gpa_max"].value = 4
            }
            // If max value is specified and min is not, set min to 0.
            if (isNaN(gpa_min_number) && !isNaN(gpa_max_number)) {
                document.forms["filter_form"]["gpa_min"].value = 0
            }
            //  If both min and max are set, validate them
            if (!isNaN(gpa_min_number) && !isNaN(gpa_max_number)) {
                if (gpa_max_number < gpa_min_number) {
                    show_err(err_field, "Max GPA value should be greater than or equal to min GPA value");
                    return false;
                }
            }
            // if all checks have passed, it is valid.
            hide_err(err_field);
            return true;
        }

        function show_err(err_field, message) {
            err_field.innerHTML = message;
            err_field.style.color = "red";
            err_field.style.visibility = "visible";
        }

        function hide_err(err_field) {
            err_field.innerHTML = "";
            err_field.style.visibility = "none";
        }