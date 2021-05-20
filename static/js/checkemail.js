$(document).ready(function(){
    $('#email').keyup( function(e){
        var email = $('#email').val();

        if(email != ''){
  
           $.ajax({
              url: '/checkemail',
              type: 'post',
              data: {email: email},
              success: function(response){
                    if (response == "Available"){
                        $('#button').prop('disabled', false);
                        $('#name_response').html(response).css({'color':'blue', 'text-align':'right'});
                    }else{
                        $('#button').prop('disabled', true);
                        $('#name_response').html(response).css({'color':'red', 'text-align':'right'});
                    }
               }
           });
        }else{
           $("#name_response").html("");
        }
    })
})