$(document).ready(function () {
   $('#username').keyup(function (e) {
      var username = $('#username').val();

      if (username != '') {

         $.ajax({
            url: '/checkusername',
            type: 'post',
            data: { username: username },
            success: function (response) {
               if (response == "Available") {
                  $('#button').prop('disabled', false);
                  $('#uname_response').html(response).css({ 'color': 'blue', 'text-align': 'right' });

               } else {
                  $('#button').prop('disabled', true);
                  $('#uname_response').html(response).css({ 'color': 'red', 'text-align': 'right' });
               }
            }
         });
      } else {
         $("#uname_response").html("");
      }
   })
})