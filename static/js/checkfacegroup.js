$(document).ready(function(){
    $('#groupname').keyup( function(e){
        var groupname = $('#groupname').val();

        if(groupname != ''){
  
           $.ajax({
              url: '/checkgroupname',
              type: 'post',
              data: {groupname: groupname},
              success: function(response){
                    if (response == "Available"){
                  $('#fname_response').html(response).css({'color':'blue', 'text-align':'right'});
                  $('#button').removeAttr('disabled');
                    }else{
                        $('#fname_response').html(response).css({'color':'red', 'text-align':'right'});
                    }
               }
           });
        }else{
           $("#fname_response").html("");
        }
    })
})