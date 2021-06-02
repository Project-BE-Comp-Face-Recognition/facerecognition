$("#teacherid").change(function () {
    const teacherId = $(this).val();  // get the selected subject ID from the HTML dropdown list 

    if (teacherId != '') {
        $.ajax({
            url: '/subjectbyid',
            type: 'post',
            data: { 'teacherId': teacherId },
            success: function (data) {   // `data` is from `get_topics_ajax` view function
                $('#subject').prop('disabled', false);

                let html_data = '<option value="" disabled selected>Select Subject</option>';
                data.forEach(function (data) {
                    html_data += `<option value="${data}">${data}</option>`
                });
                
                $("#subject").html(html_data); // replace the contents of the topic input with the data that came from the server
            }
        });
    } else {
        $("#fname_response").html("");
    }
});