$("#addRow").click(function () {
        var html = '';
        html += '<div id="inputFormRow">';
        html += '<div class="input-group mb-3">';
        html += '<input type="text" name="title[]" class="form-control m-input" placeholder="Enter Subject " autocomplete="off">';
        html += '<div class="input-group-append">';
        html += '<button id="removeRow" type="button" class="btn btn-danger">Remove</button>';
        html += '</div>';
        html += '</div>';

        $('#newRow').append(html);
    });

    // remove row
    $(document).on('click', '#removeRow', function () {
        $(this).closest('#inputFormRow').remove();
    });


// $(function() {
//         $("#symbol").click(function (e) {
//           e.preventDefault();
//           $("#myform").append('<input type="text" class="form-control form-control-user" placeholder="Enter Subject">');
//           $(".dynamic_field_focus").last().focus();
//         });
  
  
//         $("body").on("click", ".dynamic_field_remove", function (e) {
//           e.preventDefault();
//           $(this).closest('.dynamic_field_div').remove();
//         });
//       });